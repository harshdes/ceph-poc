package com.wdc.fios.model;

import java.util.SortedSet;

/**
 * Created by 25200 on 11/21/16.
 */
public class ParamAddUser {
    private String name;
    private String password;
    private SortedSet<String> emails;

    public ParamAddUser() { }

    public ParamAddUser(String name, String password, SortedSet<String> emails) {
        this.name = name;
        this.password = password;
        this.emails = emails;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public SortedSet<String> getEmails() {
        return emails;
    }

    public void setEmails(SortedSet<String> emails) {
        this.emails = emails;
    }
}
