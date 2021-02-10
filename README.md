# itsm_finder

nodejs 와 Python Flask 간 웹 API 통신 예제 포함

아래 테이블 match - against 필요

CREATE TABLE IF NOT EXISTS `hmmpi`.`itsm_master` (
  `itsm_ref` char(15),
  `itsm_summary` varchar(250),
  `itsm_description` TEXT,
  `itsm_input_date` char(20),
  FULLTEXT KEY itsm_summary (itsm_summary)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

alter table `hmmpi`.`itsm_master` add FULLTEXT(itsm_summary, itsm_description);

select distinct itsm_ref, itsm_summary, itsm_description from `hmmpi`.`itsm_master`
where match(itsm_summary, itsm_description) against ('manifest') AND itsm_ref like 'HSD%'
limit 10;
