package com.wdc.fios.repository;

import com.wdc.fios.model.Task;
import org.springframework.data.repository.CrudRepository;

public interface TaskRepository extends CrudRepository<Task, String> {
    Task getTaskById(String id);
}
