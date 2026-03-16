#!/usr/bin/env python3
"""Raft consensus — leader election and log replication simulation."""
import random
class RaftNode:
    def __init__(self,id,peers):
        self.id=id;self.peers=peers;self.state="follower"
        self.term=0;self.voted_for=None;self.log=[];self.commit_idx=0
    def start_election(self):
        self.term+=1;self.state="candidate";self.voted_for=self.id;votes=1
        for p in self.peers:
            if random.random()>0.3: votes+=1
        if votes>len(self.peers)//2: self.state="leader"
        else: self.state="follower"
    def append_entry(self,entry):
        if self.state!="leader": return False
        self.log.append({"term":self.term,"data":entry});return True
class RaftCluster:
    def __init__(self,n):
        ids=list(range(n));self.nodes=[RaftNode(i,[j for j in ids if j!=i]) for i in ids]
    def elect_leader(self):
        candidate=random.choice(self.nodes);candidate.start_election()
        if candidate.state=="leader":
            for n in self.nodes:
                if n!=candidate: n.state="follower"
        return candidate if candidate.state=="leader" else None
def main():
    random.seed(42);cluster=RaftCluster(5)
    leader=None
    for _ in range(10):
        leader=cluster.elect_leader()
        if leader: break
    if leader: print(f"Leader: node {leader.id}, term {leader.term}")
if __name__=="__main__":main()
