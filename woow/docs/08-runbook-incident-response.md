
# Incident Response

**Pause trading**: `kubectl -n <ns> scale deploy <agent> --replicas=0`  
**Flip to SIM**: `agent.mode=SIM` in values; sync via Argo CD.  
**Check stream health** and account endpoints before resuming. citeturn0search19
