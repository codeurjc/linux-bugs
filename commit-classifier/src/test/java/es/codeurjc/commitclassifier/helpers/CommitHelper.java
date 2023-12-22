package es.codeurjc.commitclassifier.helpers;

import java.util.Map;

import com.fasterxml.jackson.databind.ObjectMapper;

import es.codeurjc.commitclassifier.model.Commit;

public class CommitHelper {

    public static String raw_json = """
        {backend_name=Git, backend_version=0.13.0, category=commit, classified_fields_filtered=null, data={Author=Linus Torvalds <torvalds@linux-foundation.org>, AuthorDate=Thu Jan 6 18:35:17 2022 -0800, Commit=Linus Torvalds <torvalds@linux-foundation.org>, CommitDate=Thu Jan 6 18:35:17 2022 -0800, Merge=b2b436ec0205 b35a0f4dd544, commit=ddec8ed2d4905d0967ce2ec432e440e582aa52c6, files=[{added=1, file=drivers/infiniband/core/uverbs_marshall.c, removed=1}, {added=3, file=drivers/infiniband/core/uverbs_uapi.c, removed=0}, {added=3, file=drivers/infiniband/hw/mlx5/mlx5_ib.h, removed=3}, {added=14, file=drivers/infiniband/hw/mlx5/mr.c, removed=12}, {added=7, file=drivers/infiniband/sw/rxe/rxe_mr.c, removed=9}], message=Merge tag 'for-linus' of git://git.kernel.org/pub/scm/linux/kernel/git/rdma/rdma

        Pull rdma fixes from Jason Gunthorpe:
         "Last pull for 5.16, the reversion has been known for a while now but
          didn't get a proper fix in time. Looks like we will have several
          info-leak bugs to take care of going foward.
        
           - Revert the patch fixing the DM related crash causing a widespread
             regression for kernel ULPs. A proper fix just didn't appear this
             cycle due to the holidays
        
           - Missing NULL check on alloc in uverbs
        
           - Double free in rxe error paths
        
           - Fix a new kernel-infoleak report when forming ah_attr's without
             GRH's in ucma"
        
        * tag 'for-linus' of git://git.kernel.org/pub/scm/linux/kernel/git/rdma/rdma:
          RDMA/core: Don't infoleak GRH fields
          RDMA/uverbs: Check for null return of kmalloc_array
          Revert "RDMA/mlx5: Fix releasing unallocated memory in dereg MR flow"
          RDMA/rxe: Prevent double freeing rxe_map_set(), parents=[b2b436ec0205abde78ef8fd438758125ffbb0fec, b35a0f4dd544eaa6162b6d2f13a2557a121ae5fd], refs=[]}, origin=linux, perceval_version=0.23.1, search_fields={item_id=ddec8ed2d4905d0967ce2ec432e440e582aa52c6}, tag=linux, timestamp=1.699829870956275E9, updated_on=1.641522917E9, uuid=93afe73637ebc587cb572dcab1553a1028a67089}
          """;

    public static Commit getCommit() {
        ObjectMapper objectMapper = new ObjectMapper();
        Map<String, Object> json = (Map<String, Object>) objectMapper.convertValue(raw_json, Map.class);
        Commit commit = new Commit(
                ((Map<String, Object>) json.get("data")).get("commit").toString(),
                json);
        return commit;
    }
}
