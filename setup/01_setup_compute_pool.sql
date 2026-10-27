/* =====================================================================
   HOL ESPM - PASSO 1 - Criar o "motor" dos notebooks (compute pool)

   Tempo: ~2 minutos (o pool pode levar 1-3 min para ficar pronto)

   Por que um segundo motor?
     - O warehouse (ESPM_WH) roda SQL.
     - Os notebooks rodam Python num "container" (um mini computador).
       Esse container mora num COMPUTE POOL, servico chamado
       Snowpark Container Services (SPCS).
   ===================================================================== */

USE ROLE ACCOUNTADMIN;

-- CPU_X64_XS: menor maquina disponivel, suficiente para a aula.
-- MIN/MAX_NODES = 1: uma maquina so (controle de custo).
-- AUTO_SUSPEND_SECS = 18000: desliga sozinho apos 5 horas sem uso.
CREATE COMPUTE POOL IF NOT EXISTS ESPM_NOTEBOOK_POOL
  MIN_NODES = 1
  MAX_NODES = 1
  INSTANCE_FAMILY = CPU_X64_XS
  AUTO_RESUME = TRUE
  AUTO_SUSPEND_SECS = 18000
  COMMENT = 'ESPM_HOL';

-- CHECKPOINT: a coluna "state" deve mostrar STARTING, IDLE ou ACTIVE
-- e "auto_suspend_secs" deve ser 18000
SHOW COMPUTE POOLS LIKE 'ESPM_NOTEBOOK_POOL';

/* PROXIMO PASSO (no Snowsight):
   1. Projects > Workspaces > menu do workspace > "From Git repository"
      URL: https://github.com/sfc-gh-dpiroto/ESPM_Evento2026
      API integration: GIT_ESPM_INT   |  Autenticacao: Public repository
   2. Abra notebooks/01_bronze_ingestao.ipynb
   3. Clique em "Connect" > Create new service:
        Compute pool: ESPM_NOTEBOOK_POOL
        Idle timeout: 4 hours (240 min)
      Todos os notebooks da aula reutilizam esse mesmo servico.
*/
