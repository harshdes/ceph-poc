package com.wdc.fios.controller;

import com.wdc.fios.exception.FiosException;
import com.wdc.fios.model.Task;
import com.wdc.fios.service.TaskService;
import com.wdc.fios.tasks.Events;
import com.wdc.fios.tasks.States;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiResponse;
import io.swagger.annotations.ApiResponses;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.statemachine.StateMachine;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

/**
 * Created by 25200 on 12/14/16.
 */
@RestController
@Api(tags = {"Ceph nodes service"})
@RequestMapping(value = "/nodes", produces = MediaType.APPLICATION_JSON_VALUE)
public class NodeController {
    private final Logger logger = LoggerFactory.getLogger(this.getClass());

    private TaskService taskService;

    @Autowired
    public NodeController(TaskService taskService) {
        this.taskService = taskService;
    }

    @ApiOperation(value = "/", notes = "Adds a new ceph node")
    @ApiResponses(
            @ApiResponse(code = 200, message = "Task ID", response =  Task.class))
    @RequestMapping(method = RequestMethod.POST, value = "")
    public ResponseEntity<Task> addNode() throws FiosException {
        StateMachine<States, Events> stateMachine = taskService.startStateMachine("addNodeTask");
        logger.debug("Adding new node using task: " + stateMachine.getUuid().toString());

        return new ResponseEntity<Task>(new Task(stateMachine.getUuid().toString(),
                stateMachine.getState().toString()), HttpStatus.OK);
    }
}
