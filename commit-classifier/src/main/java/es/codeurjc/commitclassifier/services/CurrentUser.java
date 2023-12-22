package es.codeurjc.commitclassifier.services;

import org.springframework.stereotype.Component;
import org.springframework.web.context.annotation.SessionScope;

@Component
@SessionScope
public class CurrentUser {

	private String name = "";

	public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
