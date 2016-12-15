package com.wdc.fios.tasks;

import com.wdc.fios.model.Task;
import com.wdc.fios.repository.TaskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.Message;
import org.springframework.statemachine.StateContext;
import org.springframework.statemachine.StateMachine;
import org.springframework.statemachine.listener.StateMachineListener;
import org.springframework.statemachine.listener.StateMachineListenerAdapter;
import org.springframework.statemachine.state.State;
import org.springframework.statemachine.transition.Transition;
import org.springframework.stereotype.Component;

/**
 * Created by 25200 on 12/15/16.
 */
public class StateMachineEventListener extends StateMachineListenerAdapter<AddNodeTask.Config.AddNodeStates, AddNodeTask.Config.AddNodeEvents>  {
//    private String uuid;
//
//    public StateMachineEventListener(String uuid, TaskRepository taskRepository) {
//        this.uuid = uuid;
//        this.taskRepository = taskRepository;
//    }
//
//    //@Autowired
//    private TaskRepository taskRepository;
//
//    @Override
//    public void stateChanged(State<AddNodeTask.Config.AddNodeStates, AddNodeTask.Config.AddNodeEvents> from,
//                             State<AddNodeTask.Config.AddNodeStates, AddNodeTask.Config.AddNodeEvents> to) {
//        System.out.println("stateChanged");
////        Task t = taskRepository.findOne(this.uuid);
////        if (t != null) {
////            t.setState(to.toString());
////            taskRepository.save(t);
////        }
//    }
}