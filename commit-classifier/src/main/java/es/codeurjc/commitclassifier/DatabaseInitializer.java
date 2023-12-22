package es.codeurjc.commitclassifier;

import java.io.File;
import java.io.IOException;
import java.net.URISyntaxException;
import java.util.Map;

import org.apache.tomcat.util.json.ParseException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import es.codeurjc.commitclassifier.model.Commit;
import es.codeurjc.commitclassifier.repositories.CommitRepository;
import jakarta.annotation.PostConstruct;

@Service
public class DatabaseInitializer {

    @Autowired
    private CommitRepository commitRepository;

    @Value("${commit.list.path}")
    private String commitListPath;

    @PostConstruct
    public void init() throws IOException, URISyntaxException, ParseException {

        if (commitRepository.findById(1L).isEmpty()) {
            ObjectMapper objectMapper = new ObjectMapper();

            JsonNode[] commit_list = objectMapper.readValue(new File(commitListPath),
                    JsonNode[].class);

            for (JsonNode commit : commit_list) {

                Map<String, Object> json = (Map<String, Object>) objectMapper.convertValue(commit, Map.class);

                commitRepository.save(
                        new Commit(
                                commit.get("data").get("commit").asText(),
                                json));
            }
        }

    }

}
