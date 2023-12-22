package es.codeurjc.commitclassifier.controller;

import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.servlet.ModelAndView;

import es.codeurjc.commitclassifier.model.Commit;
import es.codeurjc.commitclassifier.model.CommitClassificationResult;
import es.codeurjc.commitclassifier.repositories.CommitRepository;
import es.codeurjc.commitclassifier.services.CommitClassificationResultService;
import es.codeurjc.commitclassifier.services.CurrentUser;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.websocket.server.PathParam;

@Controller
public class CommitController {

	@Autowired
	private CommitRepository commitRepository;

	@Autowired
	private CommitClassificationResultService commitClassificationResultService;

	@Autowired
	private CurrentUser currentUser;

	@GetMapping("/")
	public String showCommits(Model model) {

		model.addAttribute("commits", commitRepository.findAll());

		return "index";
	}

	@GetMapping("/commit/{id}")
	public String getCommit(Model model, @PathVariable long id, @PathParam("hasMessage") boolean hasMessage) {

		Commit commit = commitRepository.findById(id).get();

		model.addAttribute("commit", commit);
		model.addAttribute("next", commit.getId() + 1);
		model.addAttribute("last", Math.max(commit.getId() - 1, 1));
		model.addAttribute("currentUser", currentUser);
		model.addAttribute("results", commitClassificationResultService.getCommitClassificationResultsByCommitHash(commit.getCommit_hash()));

		if (hasMessage) {
			model.addAttribute("hasMessage", true);
			model.addAttribute("message", "Message");
		}

		return "commit";
	}

	@PostMapping("/commit/{commit_id}/classification")
	public ModelAndView saveClassification(Model model, @PathVariable long commit_id,
			CommitClassificationResult classification) {

		commitClassificationResultService.saveCommitClassificationResult(classification);

		model.addAttribute("hasMessage", true);
		currentUser.setName(classification.getReviewer());

		return new ModelAndView("redirect:/commit/" + commit_id, model.asMap());
	}

	@GetMapping("/api/results.csv")
	public void exportCsv(HttpServletResponse response, @PathParam("download") boolean download) throws IOException {
		
		response.setCharacterEncoding(StandardCharsets.UTF_8.name());

		if(download){
			response.setContentType("text/csv");
			response.setHeader("Content-Disposition", "attachment; filename=results.csv");
		}else{
			response.setContentType("text/plain");

		}

		try (Writer writer = new OutputStreamWriter(response.getOutputStream(), StandardCharsets.UTF_8)) {
			writer.write("id,commit_hash,reviewer,is_bug_fixing_commit,is_obvious_bug,is_safety_related,type_of_safety_related,comment,link_visited\n");
			List<CommitClassificationResult> results = commitClassificationResultService
					.getCommitClassificationResults();
			for (CommitClassificationResult r : results) {
				writer.write(String.format("%d,%s,%s,%s,%s,%s,%s,%s,%s\n", 
					r.getId(), 
					r.getCommit_hash(),
					r.getReviewer(),
					r.getIs_bug_fixing_commit(),
					r.getIs_obvious_bug(),
					r.getIs_safety_related(),	
					r.getType_of_safety_related(),	
					r.getComment(),
					r.isLink_visited()
				));
			}
			writer.flush();
		}
	}

}
