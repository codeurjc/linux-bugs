package es.codeurjc.commitclassifier.utils;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ModelAttribute;

@ControllerAdvice
public class GlobalControllerAdvice {

    @Value("${app.version}")
    private String version;

    @ModelAttribute("version")
    public String getVersion() {
        return version;
    }
}
