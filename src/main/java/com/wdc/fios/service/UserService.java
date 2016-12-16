package com.wdc.fios.service;

import com.wdc.fios.exception.FiosException;
import com.wdc.fios.model.ParamAddUser;
import com.wdc.fios.repository.UserRepository;
import com.wdc.fios.model.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by 25200 on 11/18/16.
 */
@Component
public class UserService {
    private final Logger logger = LoggerFactory.getLogger(this.getClass());

    private UserRepository userRepository;

    @Autowired
    public UserService(UserRepository userRepository){
        this.userRepository = userRepository;
    }

    public User getUserByName(String name) throws Exception {
        User u = userRepository.getUserByName(name);
        if (u == null) {
            logger.error("User " + name + " not found");
            // TODO introduce catalog for codes and messages
            throw new FiosException(1, "User " + name + " not found");
        }
        return u;
    }

    public List<User> getUsers()  {
        List<User> response = new ArrayList<User>();
        for (User u : userRepository.findAll()) {
            response.add(u);
        }
        return response;
    }

    public User addUser(ParamAddUser in) {
        User u = new User(in.getName(), in.getPassword(), in.getEmails());
        return userRepository.save(u);
    }

    public void delete(String name) throws Exception {
        User u = this.getUserByName(name);
        if (u != null)
            userRepository.delete(u);
    }
}
