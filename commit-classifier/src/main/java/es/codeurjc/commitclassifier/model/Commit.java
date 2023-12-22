package es.codeurjc.commitclassifier.model;

import java.util.Map;

import es.codeurjc.commitclassifier.utils.HashMapConverter;
import jakarta.persistence.Column;
import jakarta.persistence.Convert;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Commit {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private long id;

    private String commit_hash;

    @Convert(converter = HashMapConverter.class)
    @Column(length = 50000)
    private Map<String, Object> json;

    public Commit() {
    }

    public Commit(String commit_hash, Map<String, Object> json) {
        this.commit_hash = commit_hash;
        this.json = json;
    }

    public long getId() {
        return this.id;
    }
    
    public String getCommit_hash() {
        return this.commit_hash;
    }

    public Map<String, Object> getJson() {
        Map<String, Object> data = (Map<String, Object>) this.json.get("data");
		String cleanedMessage = data.get("message").toString()
            .replaceAll("Fixes:.*", "")
            .replace("\n\n", "<br>")
            .replace("\n", "<br>")
        ;
		data.put("message", cleanedMessage);
        return this.json;
    }

}
