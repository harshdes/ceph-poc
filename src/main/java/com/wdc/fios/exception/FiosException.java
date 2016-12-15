package com.wdc.fios.exception;

/**
 * Created by 25200 on 12/15/16.
 */
// TODO localization, catalog etc
public class FiosException extends  Exception {
    protected int messageCode; // use from a common catalog understood by clients

    public FiosException(int messageCode, String message) {
        super(message);
        this.messageCode = messageCode;
    }

    public int getMessageCode() {
        return messageCode;
    }
}
