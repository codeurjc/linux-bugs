package es.codeurjc.commitclassifier.repositories;

import org.springframework.data.jpa.repository.JpaRepository;

import es.codeurjc.commitclassifier.model.Commit;

public interface CommitRepository extends JpaRepository<Commit, Long> {
    
}
