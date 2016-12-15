package com.wdc.fios.service;

import com.wdc.fios.exception.FiosException;
import com.wdc.fios.model.Task;
import com.wdc.fios.repository.TaskRepository;
import com.wdc.fios.tasks.Events;
import com.wdc.fios.tasks.States;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.statemachine.StateContext;
import org.springframework.statemachine.StateMachine;
import org.springframework.statemachine.config.ObjectStateMachineFactory;
import org.springframework.statemachine.config.StateMachineFactory;
import org.springframework.statemachine.support.StateMachineInterceptor;
import org.springframework.statemachine.support.StateMachineInterceptorAdapter;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

@Component
public class TaskService {
    private TaskRepository taskRepository;
    private ApplicationContext appContext;

    @Autowired
    public TaskService(TaskRepository taskRepository, ApplicationContext appContext){
        this.taskRepository = taskRepository;
        this.appContext = appContext;
    }

    public List<Task> getTasks()  {
        List<Task> response = new ArrayList<>();
        for (Task t : taskRepository.findAll()) {
            response.add(t);
        }
        return response;
    }

    public StateMachine<States, Events> startStateMachine(String taskName) throws FiosException {
        StateMachineFactory<States, Events> stateMachineFactory =
                appContext.getBean(taskName, ObjectStateMachineFactory.class);
        if (stateMachineFactory == null) {
            // TODO introduce a catalog for exception codes
            throw new FiosException(1, "Could not find state machine factory for task " + taskName);
        }

        StateMachine<States, Events> stateMachine = stateMachineFactory.getStateMachine();
        // TODO instead of using toString() on state, model it or save directly into database. toString() isn't useful
        taskRepository.save(new Task(stateMachine.getUuid().toString(), null));

        // Add interceptor to perform bookkeeping during state transitions
        stateMachine.getStateMachineAccessor()
                .withRegion().addStateMachineInterceptor(new StateMachineInterceptorAdapter<States, Events>() {
                    @Override
                    public StateContext<States, Events> postTransition(StateContext<States, Events> stateContext) {
                        Task t = taskRepository.getTaskById(stateMachine.getUuid().toString());
                        if (t != null) {
                            t.setState(stateMachine.getState().toString());
                            taskRepository.save(t);
                        }
                        return stateContext;
                    }
        });

        stateMachine.start();

        return stateMachine;
    }
}
