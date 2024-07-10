CREATE TABLE basic_information ( 
        `protein_id` INT primary key,  -- 即 index
        `ECNumber` text NOT NULL, -- length <= 16
        `ProteinName` text NOT NULL, -- length <= 100
        `Organism` text, -- length <= 100
        `UniprotID` text, -- length <= 100
        `Sequence` text,  -- length <= 2000
        `SequenceLength` SMALLINT, -- [1, 9999]
        `PDBID_WT` text,  -- length <= 4
        `PDBID_MUT` text,  -- length <= 4
        `AlphaFoldDB` text,  -- length <= 100
        `Mutation` text,  -- length <= 100
        `MutatedChain` text,  -- length <= 10
        `MutationCount` SMALLINT -- [1, 9999]
);
CREATE INDEX basic_information_basic_cols_gin 
ON basic_information 
USING gin (
                `ECNumber` gin_bigm_ops,
                `ProteinName` gin_bigm_ops,
                `UniprotID` gin_bigm_ops,
                `Organism`,
                `PDBID_WT` gin_bigm_ops,
                `PDBID_MUT` gin_bigm_ops,
                `Mutation` gin_bigm_ops,
                `MutationCount`
);
CREATE INDEX basic_information_sequence_length_btree 
ON basic_information 
USING BTREE (
                `SequenceLength`
);



CREATE TABLE substrate ( 
        `protein_id` INT primary key,  -- 即 index，关联 basic_information 表的 protein_id
        `Substrate` text,   -- length <= 100
        `Smiles` text, -- length <= 1000
        `MolecularFormula` text, -- length <= 1000
        `Cofator` text, -- length <= 1000
        `ProductFormula` text -- length <= 1000
);
CREATE INDEX substrate_basic_cols_gin 
ON substrate
USING gin (
                `Substrate` gin_bigm_ops
);



CREATE TABLE kinetic_parameters ( 
        `protein_id` INT primary key,  -- 即 index，关联 basic_information 表的 protein_id
        `Activity` DECIMAL(11,5), 
        `KM` DECIMAL(11,5), 
        `Kcat` DECIMAL(11,5), 
        `KMPerKcat` DECIMAL(11,5),
        `TN` DECIMAL(11,5),
        `EValue` DECIMAL(11,5), 
        `DeltaDeltaG` DECIMAL(11,5),
        `Temperature` SMALLINT, 
        `pH` DECIMAL(7,5)
);
CREATE INDEX kinetic_parameters_activity_btree 
ON kinetic_parameters
USING BTREE (
                `Activity`
);
CREATE INDEX kinetic_parameters_km_btree 
ON kinetic_parameters
USING BTREE (
                `KM`
);
CREATE INDEX kinetic_parameters_kcat_btree 
ON kinetic_parameters
USING BTREE (
                `kcat`
);
CREATE INDEX kinetic_parameters_kmperkcat_btree 
ON kinetic_parameters
USING BTREE (
                `KMPerKcat`
);
CREATE INDEX kinetic_parameters_tn_btree 
ON kinetic_parameters
USING BTREE (
                `TN`
);
CREATE INDEX kinetic_parameters_evalue_btree 
ON kinetic_parameters
USING BTREE (
                `EValue`
);
CREATE INDEX kinetic_parameters_deltadeltag_btree 
ON kinetic_parameters
USING BTREE (
                `DeltaDeltaG`
);
CREATE INDEX kinetic_parameters_temperature_btree 
ON kinetic_parameters
USING BTREE (
                `Temperature`
);
CREATE INDEX kinetic_parameters_ph_btree 
ON kinetic_parameters
USING BTREE (
                `pH`
);



CREATE TABLE structure_information ( 
        `protein_id` INT primary key,  -- 即 index，关联 basic_information 表的 protein_id
        `RSA` DECIMAL(11,5), 
        `PHI` DECIMAL(11,5), 
        `PSI` DECIMAL(11,5), 
        `ResidueDepth` DECIMAL(11,5),
        `CADepth` DECIMAL(11,5),
        `RelativeBfactor` DECIMAL(11,5) 
);



CREATE TABLE reaction_calculation ( 
        `protein_id` INT primary key,  -- 即 index，关联 basic_information 表的 protein_id
        `ActiveResidue` text,  -- length <= 1000
        `ReactionSmile` text,  -- length <= 1000
        `KEGG` text,  -- length <= 100
        `ReactionEnergy` DECIMAL(11,5), 
        `ReactionParameters` text -- length <= 1000
);



CREATE TABLE comment ( 
        `protein_id` INT primary key,  -- 即 index，关联 basic_information 表的 protein_id
        `Literature` text,  -- length <= 10000
        `DOI` text,  -- length <= 10000
        `Year` SMALLINT, 
        `PMID` text  -- length <= 100
);
CREATE INDEX comment_year_btree 
ON comment
USING BTREE (
                `Year`
);
CREATE INDEX comment_basic_cols_gin 
ON comment
USING gin (
                `PMID`
);


-- 用户表
CREATE TABLE user ( 
        `user_id` SERIAL primary key, -- 唯一id, 自增 int
        `email` text unique, -- 邮箱
        `password` text, -- 加密后的密码
        `name` text, -- 昵称？需要吗
        `is_admin` boolean DEFAULT FALSE -- 是否管理员？true 则为管理员
);
CREATE INDEX user_email_and_password_btree 
ON user
USING BTREE (
                `email`,
                `password`
);