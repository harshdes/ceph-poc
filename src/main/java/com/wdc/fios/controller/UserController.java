package com.wdc.fios.controller;

import java.util.List;

import com.wdc.fios.model.ParamAddUser;
import com.wdc.fios.model.User;
import com.wdc.fios.service.UserService;
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
import org.springframework.web.bind.annotation.*;

/**
 * Created by 25200 on 11/18/16.
 */
@RestController
@RequestMapping(value = "/users", produces = MediaType.APPLICATION_JSON_VALUE)
@Api(tags = {"Ceph users service"})
public class UserController {
    private final Logger logger = LoggerFactory.getLogger(this.getClass());

    private UserService userService;

    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }

    @ApiOperation(value = "", notes = "Get all users")
    @ApiResponses(
            @ApiResponse(code = 200, message = "", response = User.class))
    @RequestMapping(method = RequestMethod.GET)
    public ResponseEntity<List<User>> getAllUsers() {
        return new ResponseEntity<>(userService.getUsers(), HttpStatus.OK);
    }

    @ApiOperation(value = "/{name}", notes = "Get a user's profile with name")
    @ApiResponses(
            @ApiResponse(code = 200, message = "", response = User.class))
    @RequestMapping(method = RequestMethod.GET, value = "/{name}")
    public ResponseEntity<User> getUserByUsername(@PathVariable("name") String name) throws Exception {
        ResponseEntity<User> entity = new ResponseEntity<User>(userService.getUserByName(name), HttpStatus.OK);
        return entity;
    }

    @ApiOperation(value = "", notes = "Adds a new user")
    @ApiResponses(
            @ApiResponse(code = 200, message = "", response = User.class))
    @RequestMapping(method = RequestMethod.POST, value = "")
    public ResponseEntity<User> addUser(@RequestBody ParamAddUser in) {
        return new ResponseEntity<>(userService.addUser(in), HttpStatus.OK);

    }

    @ApiOperation(value = "/{name}", notes = "Deletes an existing user user")
    @ApiResponses(
            @ApiResponse(code = 200, message = "", response = Void.class))
    @RequestMapping(method = RequestMethod.DELETE, value = "/{name}")
    public ResponseEntity<Void> delete(@PathVariable("name") String name) throws Exception {
        userService.delete(name);
        return ResponseEntity.noContent().build();
    }
}
