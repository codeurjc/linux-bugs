package es.codeurjc.commitclassifier.services;

import static org.springframework.data.domain.ExampleMatcher.GenericPropertyMatchers.ignoreCase;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Example;
import org.springframework.data.domain.ExampleMatcher;
import org.springframework.stereotype.Service;

import es.codeurjc.commitclassifier.model.CommitClassificationResult;
import es.codeurjc.commitclassifier.repositories.CommitClassificationResultRepository;

@Service
public class CommitClassificationResultService{

    @Autowired
    private CommitClassificationResultRepository commitClassificationResultRepository;

	public List<CommitClassificationResult> getCommitClassificationResultsByCommitHash(String commit_hash) {
		ExampleMatcher modelMatcher = ExampleMatcher.matching()
			.withIgnorePaths("id", 
					"reviewer",
                    "is_bug_fixing_commit",
					"is_obvious_bug",
                    "is_safety_related",
			        "type_of_safety_related",
			        "comment",
                    "link_visited"
            ) 
			.withMatcher("commit_hash", ignoreCase());
		var commitClassificationResult = new CommitClassificationResult();
		commitClassificationResult.setCommit_hash(commit_hash);
		Example<CommitClassificationResult> example = Example.of(commitClassificationResult, modelMatcher);
		return commitClassificationResultRepository.findAll(example);
	}

    public void saveCommitClassificationResult(CommitClassificationResult commitClassificationResult){
        ExampleMatcher modelMatcher = ExampleMatcher.matching()
			.withIgnorePaths("id", 
                    "is_bug_fixing_commit",
					"is_obvious_bug",
                    "is_safety_related",
			        "type_of_safety_related",
			        "comment",
                    "link_visited"
            ) 
			.withMatcher("reviewer", ignoreCase());
		
		Example<CommitClassificationResult> example = Example.of(commitClassificationResult, modelMatcher);
		Optional<CommitClassificationResult> op = commitClassificationResultRepository.findOne(example);

		if(op.isPresent()){
			// UPDATE
			commitClassificationResult.setId(op.get().getId());
			commitClassificationResultRepository.save(commitClassificationResult);
		}else{
			// INSERT
			commitClassificationResultRepository.save(commitClassificationResult);
		}
    }

    public List<CommitClassificationResult> getCommitClassificationResults(){
        return commitClassificationResultRepository.findAll();
    }

}