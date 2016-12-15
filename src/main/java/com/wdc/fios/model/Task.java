package com.wdc.fios.model;

import org.springframework.data.cassandra.mapping.PrimaryKey;
import org.springframework.data.cassandra.mapping.Table;

/**
 * Created by 25200 on 12/15/16.
 */
@Table(value = "tasks")
public class Task {
    @PrimaryKey
    private String id;
    private String state;

    public Task() {
    }

    public Task(String id, String state) {
        this.id = id;
        this.state = state;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }
}
