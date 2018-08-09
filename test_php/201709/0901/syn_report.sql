create table wifilz_syn_report (
`report_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
`report_text` longtext NOT NULL,
`report_data` text NOT NULL,
`report_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (`report_id`)
)ENGINE=MyISAM charset=utf8;
