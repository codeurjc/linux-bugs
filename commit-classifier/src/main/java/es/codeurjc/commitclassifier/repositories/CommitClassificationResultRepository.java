package es.codeurjc.commitclassifier.repositories;

import org.springframework.data.jpa.repository.JpaRepository;

import es.codeurjc.commitclassifier.model.Commit;
import es.codeurjc.commitclassifier.model.CommitClassificationResult;

public interface CommitClassificationResultRepository extends JpaRepository<CommitClassificationResult, Long> {
    
}
