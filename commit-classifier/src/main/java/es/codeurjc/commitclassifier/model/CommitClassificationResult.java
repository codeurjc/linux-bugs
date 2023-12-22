package es.codeurjc.commitclassifier.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class CommitClassificationResult {

	@Id
	@GeneratedValue(strategy = GenerationType.AUTO)
	private long id;

	private String commit_hash;
	private String reviewer;
	private String is_bug_fixing_commit;
	private String is_obvious_bug;
	private String is_safety_related;
	private String type_of_safety_related;
	@Column(columnDefinition = "LONGTEXT")
	private String comment;
	private boolean link_visited = false;

	

	public CommitClassificationResult(String commit_hash, String reviewer, String is_bug_fixing_commit,
			String is_obvious_bug, String is_safety_related, String type_of_safety_related, String comment,
			boolean link_visited) {
		this.commit_hash = commit_hash;
		this.reviewer = reviewer;
		this.is_bug_fixing_commit = is_bug_fixing_commit;
		this.is_obvious_bug = is_obvious_bug;
		this.is_safety_related = is_safety_related;
		this.type_of_safety_related = type_of_safety_related;
		this.comment = comment;
		this.link_visited = link_visited;
	}

	public CommitClassificationResult() {
	}

	public long getId() {
		return id;
	}

	public void setId(long id) {
		this.id = id;
	}

	public String getCommit_hash() {
		return commit_hash;
	}

	public void setCommit_hash(String commit_hash) {
		this.commit_hash = commit_hash;
	}

	public String getReviewer() {
		return reviewer;
	}

	public void setReviewer(String reviewer) {
		this.reviewer = reviewer;
	}

	public String getIs_bug_fixing_commit() {
		return is_bug_fixing_commit;
	}

	public void setIs_bug_fixing_commit(String is_bug_fixing_commit) {
		this.is_bug_fixing_commit = is_bug_fixing_commit;
	}

	public String getIs_obvious_bug() {
		return is_obvious_bug;
	}

	public void setIs_obvious_bug(String is_obvious_bug) {
		this.is_obvious_bug = is_obvious_bug;
	}

	public String getIs_safety_related() {
		return is_safety_related;
	}

	public void setIs_safety_related(String is_safety_related) {
		this.is_safety_related = is_safety_related;
	}

	public String getType_of_safety_related() {
		return type_of_safety_related;
	}

	public void setType_of_safety_related(String type_of_safety_related) {
		this.type_of_safety_related = type_of_safety_related;
	}

	public String getComment() {
		return comment;
	}

	public void setComment(String comment) {
		this.comment = comment;
	}

	public boolean isLink_visited() {
		return link_visited;
	}

	public void setLink_visited(boolean link_visited) {
		this.link_visited = link_visited;
	}

	@Override
	public String toString() {
		return "CommitClassificationResult [id=" + id + ", commit_hash=" + commit_hash + ", reviewer=" + reviewer
				+ ", is_bug_fixing_commit=" + is_bug_fixing_commit + ", is_obvious_bug=" + is_obvious_bug
				+ ", is_safety_related=" + is_safety_related + ", type_of_safety_related=" + type_of_safety_related
				+ ", comment=" + comment + ", link_visited=" + link_visited + "]";
	}

}
