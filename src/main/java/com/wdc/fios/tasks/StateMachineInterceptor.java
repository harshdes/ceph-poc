package com.wdc.fios.tasks;

import org.springframework.messaging.Message;
import org.springframework.statemachine.StateContext;
import org.springframework.statemachine.StateMachine;
import org.springframework.statemachine.state.State;
import org.springframework.statemachine.support.StateMachineInterceptor;
import org.springframework.statemachine.support.StateMachineInterceptorAdapter;
import org.springframework.statemachine.transition.Transition;

/**
 * Created by 25200 on 12/15/16.
 */
class FiosStateMachineInterceptor extends StateMachineInterceptorAdapter<States, Events> {
    @Override
    public StateContext<States, Events> preTransition(StateContext<States, Events> stateContext) {

        return stateContext;
    }
}
