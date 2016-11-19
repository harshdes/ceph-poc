package com.wdc.fios.controller;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiResponse;
import io.swagger.annotations.ApiResponses;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Created by 25200 on 11/18/16.
 */
@RestController
@Api(tags = {"Ceph application"})
public class HomeController {
    @ApiOperation(value = "/", notes = "Welcomes user")
    @ApiResponses(
            @ApiResponse(code = 200, message = "", response = String.class))
    @RequestMapping("/")
    public String index() {
        return "Greetings from Spring Boot!";
    }

}
