package com.wdc.fios.repository;

import com.wdc.fios.model.User;
import org.springframework.data.repository.CrudRepository;

/**
 * Created by hdesai on 11/18/16.
 */
public interface UserRepository extends CrudRepository<User, String> {
    User getUserByName(String name);
}
