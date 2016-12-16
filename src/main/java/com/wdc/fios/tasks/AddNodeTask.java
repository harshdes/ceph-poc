package com.wdc.fios.tasks;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.statemachine.action.Action;
import org.springframework.statemachine.config.EnableStateMachineFactory;
import org.springframework.statemachine.config.EnumStateMachineConfigurerAdapter;
import org.springframework.statemachine.config.builders.StateMachineStateConfigurer;
import org.springframework.statemachine.config.builders.StateMachineTransitionConfigurer;

/**
 * Created by Harsh Desai on 12/14/16.
 */
@Configuration
public class AddNodeTask {

    @Configuration
    @EnableStateMachineFactory(name="addNodeTask")
    public static class Config extends EnumStateMachineConfigurerAdapter<Config.AddNodeStates, Config.AddNodeEvents> {
        private final Logger logger = LoggerFactory.getLogger(this.getClass());

        @Override
        public void configure(StateMachineStateConfigurer<AddNodeStates, AddNodeEvents> states)
                throws Exception {
            states
                    .withStates()
                    .initial(AddNodeStates.SETUP_CASSANDRA)
                    .state(AddNodeStates.SETUP_CASSANDRA, setupCassandra(), null)
                    .state(AddNodeStates.SETUP_SPRINGBOOT, setupSpringBoot(), null)
                    .state(AddNodeStates.SETUP_KEEPALIVED, setupKeepalived(), null)
                    .state(AddNodeStates.DONE)
                    .end(AddNodeStates.DONE);
        }

        @Override
        public void configure(StateMachineTransitionConfigurer<AddNodeStates, AddNodeEvents> transitions) throws Exception {
            transitions
                    .withExternal()
                    .source(AddNodeStates.SETUP_CASSANDRA).target(AddNodeStates.SETUP_SPRINGBOOT).event(AddNodeEvents.CASSANDRA_UP)
                    .and()
                    .withExternal()
                    .source(AddNodeStates.SETUP_SPRINGBOOT).target(AddNodeStates.SETUP_KEEPALIVED).event(AddNodeEvents.SPRINGBOOT_UP)
                    .and()
                    .withExternal()
                    .source(AddNodeStates.SETUP_KEEPALIVED).target(AddNodeStates.DONE).event(AddNodeEvents.KEEPALIVED_DONE);
        }

        @Bean
        public Action<AddNodeStates, AddNodeEvents> setupCassandra() {
            return stateContext -> {
                logger.debug("[state] setupCassandra");
                stateContext.getStateMachine().sendEvent(AddNodeEvents.CASSANDRA_UP);
            };
        }


        @Bean
        public Action<AddNodeStates, AddNodeEvents> setupSpringBoot() {
            return stateContext -> {
                logger.debug("[state] setupSpringBoot");
                stateContext.getStateMachine().sendEvent(AddNodeEvents.SPRINGBOOT_UP);
            };
        }

        @Bean
        public Action<AddNodeStates, AddNodeEvents> setupKeepalived() {
            return stateContext -> {
                logger.debug("[state] setupKeepalived");
                stateContext.getStateMachine().sendEvent(AddNodeEvents.KEEPALIVED_DONE);
            };
        }

        public enum AddNodeStates implements States {
            SETUP_CASSANDRA, SETUP_SPRINGBOOT, SETUP_KEEPALIVED, DONE
        }

        public enum AddNodeEvents implements Events {
            CASSANDRA_UP, SPRINGBOOT_UP, KEEPALIVED_DONE
        }
    }
}

