/* =====================================================================
   HOL ESPM - Pipeline de Dados para Martech
   PASSO 01 - Conectar o Snowflake ao GitHub da aula

   Onde rodar: Snowsight > Projects > Workspaces > + > SQL File
   Como: rode os passos 1 e 2 (prontos); depois complete os ??? dos
         passos 3 a 5 e rode o restante.
   Tempo: ~10 minutos

   O que este script faz, em linguagem simples:
     1. Liga um "motor" pequeno para rodar as consultas (warehouse)
     2. Cria o "armario" do projeto (database) com 3 gavetas:
        BRONZE (dado cru), SILVER (dado limpo), GOLD (dado pronto pro negocio)
     3. [VOCE ESCREVE] Autoriza o Snowflake a ler o GitHub da aula
     4. [VOCE ESCREVE] Cria uma copia do repositorio dentro do Snowflake
   ===================================================================== */

-- Usamos o papel de administrador da conta trial (voce ja e o dono dela)
USE ROLE ACCOUNTADMIN;

-- 1. MOTOR: warehouse e o "computador" que executa SQL.
--    XSMALL e o menor tamanho. AUTO_SUSPEND = 60 desliga sozinho apos
--    1 minuto parado, para nao gastar creditos a toa.
CREATE WAREHOUSE IF NOT EXISTS ESPM_WH
  WAREHOUSE_SIZE = XSMALL
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE
  COMMENT = 'ESPM_HOL';
USE WAREHOUSE ESPM_WH;

-- 2. ARMARIO E GAVETAS: database + schemas da arquitetura medalhao
CREATE DATABASE IF NOT EXISTS ESPM_HOL COMMENT = 'ESPM_HOL';
CREATE SCHEMA IF NOT EXISTS ESPM_HOL.BRONZE   COMMENT = 'Dado cru, do jeito que chegou';
CREATE SCHEMA IF NOT EXISTS ESPM_HOL.SILVER   COMMENT = 'Dado limpo e padronizado';
CREATE SCHEMA IF NOT EXISTS ESPM_HOL.GOLD     COMMENT = 'Metricas prontas para o negocio';
CREATE SCHEMA IF NOT EXISTS ESPM_HOL.GOLD_DBT COMMENT = 'Metricas geradas pelo dbt';
CREATE SCHEMA IF NOT EXISTS ESPM_HOL.APPS     COMMENT = 'Apps Streamlit';

/* =====================================================================
   EXERCICIO - Conecte o Snowflake ao GitHub VOCE MESMO

   Complete os ??? abaixo e rode. Use EXATAMENTE os nomes GIT_ESPM_INT e
   HOL_REPO: os notebooks seguintes dependem deles.

   Material de apoio:
     - URL do repositorio da aula: https://github.com/sfc-gh-dpiroto/ESPM_Evento2026
     - Documentacao: pesquise "CREATE GIT REPOSITORY" em docs.snowflake.com
     - Travou? Peca ao Cortex Code:
       "Crie uma API integration chamada GIT_ESPM_INT para o GitHub publico
        https://github.com/sfc-gh-dpiroto/ e um GIT REPOSITORY chamado
        ESPM_HOL.PUBLIC.HOL_REPO apontando para o repositorio da aula"
   ===================================================================== */

-- 3. AUTORIZACAO: a API integration diz "o Snowflake pode falar com
--    estes enderecos do GitHub". Repositorio publico = sem senha.
--    Dica: o provedor para Git via HTTPS e git_https_api; o prefixo
--    permitido e o endereco do dono do repositorio (termina com /).
CREATE API INTEGRATION IF NOT EXISTS GIT_ESPM_INT
  API_PROVIDER = ???
  API_ALLOWED_PREFIXES = ('???')
  ENABLED = TRUE
  COMMENT = 'ESPM_HOL';

-- 4. COPIA DO REPOSITORIO: vira uma "pasta" dentro do Snowflake.
--    Dica: use a integration criada acima e a URL do repositorio + .git
CREATE GIT REPOSITORY IF NOT EXISTS ESPM_HOL.PUBLIC.HOL_REPO
  API_INTEGRATION = ???
  ORIGIN = '???'
  COMMENT = 'ESPM_HOL';

-- 5. Busque a versao mais recente do GitHub (rode de novo se o professor avisar)
--    Dica: ALTER GIT REPOSITORY <nome> FETCH;
???;

-- CHECKPOINT: voce deve ver 9 arquivos .csv
LS @ESPM_HOL.PUBLIC.HOL_REPO/branches/main/data/;

/* PROXIMO PASSO: rode 01_setup/02_setup_compute_pool.sql */
