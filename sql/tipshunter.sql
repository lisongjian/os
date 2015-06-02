-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2014-08-06 14:21:55
-- 服务器版本: 5.5.37-0ubuntu0.14.04.1
-- PHP 版本: 5.5.9-1ubuntu4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `tipshunter`
--

-- --------------------------------------------------------

--
-- 表的结构 `ad_config`
--

CREATE TABLE IF NOT EXISTS `ad_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ad_id` tinyint(4) NOT NULL,
  `title` varchar(20) COLLATE utf8_unicode_ci NOT NULL COMMENT '渠道简称（别名）',
  `intro` varchar(15) COLLATE utf8_unicode_ci NOT NULL COMMENT '短描述',
  `detail` varchar(100) COLLATE utf8_unicode_ci NOT NULL COMMENT '详细',
  `credits` varchar(10) COLLATE utf8_unicode_ci NOT NULL COMMENT '积分数',
  `icon` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `aos_status` tinyint(1) NOT NULL,
  `ios_status` tinyint(1) NOT NULL,
  `description` varchar(10) COLLATE utf8_unicode_ci NOT NULL COMMENT '广告平台',
  `priority` tinyint(3) unsigned NOT NULL COMMENT '排序',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=3 ;

--
-- 转存表中的数据 `ad_config`
--

INSERT INTO `ad_config` (`id`, `ad_id`, `title`, `intro`, `detail`, `credits`, `icon`, `aos_status`, `ios_status`, `description`, `priority`) VALUES
(1, 1, '1', '任务A', '任务A', '50个', 'YELLOW.png', 1, 1, 'Tapjoy', 0),
(2, 2, 'Metaps', 'Metaps', 'Metaps', '50万+', 'BLUE.png', 1, 0, 'Metaps', 0);

-- --------------------------------------------------------

--
-- 表的结构 `callback_order`
--

CREATE TABLE IF NOT EXISTS `callback_order` (
  `id` int(8) NOT NULL AUTO_INCREMENT,
  `order` varchar(100) DEFAULT NULL,
  `oid` int(11) unsigned DEFAULT NULL COMMENT '全局订单ID',
  `ad` varchar(20) DEFAULT NULL,
  `adid` varchar(50) DEFAULT NULL,
  `user` int(8) unsigned NOT NULL,
  `chn` int(2) DEFAULT NULL COMMENT '渠道号',
  `points` int(4) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `device` varchar(40) DEFAULT NULL,
  `sig` varchar(40) DEFAULT NULL COMMENT '验证签名',
  `platform` int(1) DEFAULT NULL COMMENT '平台类型，3:aos,5:ios',
  `ad_source` tinyint(3) unsigned DEFAULT NULL COMMENT '广告平台',
  PRIMARY KEY (`id`),
  KEY `user` (`user`),
  KEY `oid` (`oid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='订单' AUTO_INCREMENT=350 ;

-- --------------------------------------------------------

--
-- 表的结构 `changelogs`
--

CREATE TABLE IF NOT EXISTS `changelogs` (
  `id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `release_time` datetime NOT NULL,
  `version` varchar(16) NOT NULL,
  `version_number` smallint(4) NOT NULL COMMENT '版本号',
  `platform` int(1) NOT NULL COMMENT '1=android,2=ios',
  `distribute_kind` tinyint(4) NOT NULL COMMENT '发布渠道',
  `changelog` tinytext NOT NULL,
  `download_url` varchar(512) NOT NULL COMMENT '下载地址',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- 转存表中的数据 `changelogs`
--

INSERT INTO `changelogs` (`id`, `release_time`, `version`, `version_number`, `platform`, `distribute_kind`, `changelog`, `download_url`) VALUES
(1, '2014-05-20 00:00:00', '1.0.0', 1, 1, 1, '第一个版本～～～', 'www.baidu.com'),
(2, '2014-07-14 16:14:00', '2.0.0', 2, 1, 2, 'the cash box version 2', 'www.google.com');

-- --------------------------------------------------------

--
-- 表的结构 `exchange_goods`
--

CREATE TABLE IF NOT EXISTS `exchange_goods` (
  `goods_id` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` mediumint(6) unsigned NOT NULL COMMENT '商品类型',
  `title` varchar(128) NOT NULL COMMENT '商品标题',
  `description` text NOT NULL COMMENT '商品描述',
  `price` decimal(10,3) unsigned NOT NULL COMMENT '商品价格',
  `points` int(11) unsigned NOT NULL COMMENT '兑换该商品所需要的积分数',
  `exchange_counts` mediumint(11) NOT NULL DEFAULT '0' COMMENT '兑换次数',
  PRIMARY KEY (`goods_id`),
  KEY `type` (`type_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=15 ;

--
-- 转存表中的数据 `exchange_goods`
--

INSERT INTO `exchange_goods` (`goods_id`, `type_id`, `title`, `description`, `price`, `points`, `exchange_counts`) VALUES
(3, 1, '支付宝20元', '支付宝提现20元，1天到帐', 20.000, 20000, 13),
(5, 3, 'Q币10个', 'Q币充值10个，2天到帐', 10.000, 10000, 5),
(6, 1, '支付宝30元', '支付宝提现30元，一天到账', 30.000, 30000, 7),
(11, 2, '话费51元', '话费51元', 51.000, 51000, 0),
(13, 1, '支付宝361元', '支付宝提现361元，1天到帐', 361.000, 361000, 0),
(14, 2, '话费300元', '话费300元', 300.000, 300000, 1);

-- --------------------------------------------------------

--
-- 表的结构 `exchange_orders`
--

CREATE TABLE IF NOT EXISTS `exchange_orders` (
  `id` int(8) unsigned NOT NULL AUTO_INCREMENT,
  `uid` int(8) unsigned NOT NULL,
  `oid` int(11) unsigned NOT NULL COMMENT '全局订单ID',
  `points` int(8) unsigned NOT NULL COMMENT '兑换单个商品所需要的积分数',
  `total_points` int(8) unsigned NOT NULL COMMENT '消费积分',
  `price` decimal(10,3) NOT NULL COMMENT '货物单价',
  `total_price` decimal(10,3) NOT NULL COMMENT '总价',
  `goods_id` int(3) unsigned NOT NULL,
  `goods_title` varchar(128) NOT NULL COMMENT '货物标题',
  `count` smallint(3) unsigned NOT NULL DEFAULT '1' COMMENT '兑换数量，默认1',
  `status` tinyint(2) NOT NULL DEFAULT '0' COMMENT '兑换状态，0：待审核，1:审核通过, 2:忽略(非法), 3:延缓',
  `num` varchar(30) DEFAULT NULL COMMENT '刮开卡片后的号码',
  `notes` text COMMENT '订单备注',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '兑换时间',
  `type_id` mediumint(6) DEFAULT NULL COMMENT '商品类型',
  `address` varchar(512) DEFAULT NULL COMMENT '收货地址',
  PRIMARY KEY (`id`),
  KEY `oid` (`oid`),
  KEY `uid` (`uid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='积分兑换' AUTO_INCREMENT=4 ;

-- --------------------------------------------------------

--
-- 表的结构 `exchange_types`
--

CREATE TABLE IF NOT EXISTS `exchange_types` (
  `id` mediumint(6) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL,
  `icon` varchar(512) NOT NULL,
  `address_type` varchar(32) NOT NULL COMMENT '需要提交的商品地址类型',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;

--
-- 转存表中的数据 `exchange_types`
--

INSERT INTO `exchange_types` (`id`, `title`, `icon`, `address_type`) VALUES
(1, '支付宝提现', 'goods/alipayicon@2x.png', 'alipay'),
(2, '话费充值', 'goods/huafeiiconicon@2x.png', 'phone_number'),
(3, 'Q币充值', 'goods/Qbiicon@2x.png', 'qq');

-- --------------------------------------------------------

--
-- 表的结构 `feedback`
--

CREATE TABLE IF NOT EXISTS `feedback` (
  `id` int(8) NOT NULL AUTO_INCREMENT,
  `user` int(8) NOT NULL,
  `content` text COLLATE utf8_unicode_ci NOT NULL,
  `mail` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '邮箱',
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=4 ;

-- --------------------------------------------------------

--
-- 表的结构 `global_orders`
--

CREATE TABLE IF NOT EXISTS `global_orders` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `uid` int(8) unsigned NOT NULL,
  `points` int(8) NOT NULL,
  `last` int(8) NOT NULL COMMENT '任务获取积分/消费前剩余积分',
  `record_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '流水生成时间',
  PRIMARY KEY (`id`),
  KEY `uid` (`uid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='积分流水' AUTO_INCREMENT=52 ;

-- --------------------------------------------------------

--
-- 表的结构 `options`
--

CREATE TABLE IF NOT EXISTS `options` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `values` int(11) NOT NULL,
  `description` varchar(100) COLLATE utf8_unicode_ci NOT NULL COMMENT '字段描述',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=9 ;

--
-- 转存表中的数据 `options`
--

INSERT INTO `options` (`id`, `key`, `values`, `description`) VALUES
(1, 'sign_prize', 200, '签到奖励积分数'),
(2, 'invite_reg_prize', 20, '邀请用户注册奖励积分数(邀请人和被邀请人)'),
(3, 'first_task', 1000, '被邀用户首次完成任务奖励积分数'),
(4, 'exchange_task', 1000, '被邀用户首次兑换物品奖励积分数'),
(5, 'invite_bonus', 20, '填写邀请码奖励积分'),
(6, 'new_user', 50, '新用户红包奖励'),
(7, 'task_id', 1, '帮抢高价，今日任务推荐'),
(8, 'exchange_rate', 1000, '积分与现金的兑换比例');

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `scopeid` varchar(20) DEFAULT NULL COMMENT 'facebook id',
  `gender` varchar(8) DEFAULT NULL COMMENT '性别',
  `name` varchar(128) DEFAULT NULL COMMENT '昵称',
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `phone` varchar(11) DEFAULT NULL COMMENT '手机',
  `alipay` varchar(25) DEFAULT NULL COMMENT '支付宝',
  `points` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '用户当前积分',
  `bind_points` int(10) NOT NULL DEFAULT '0' COMMENT '绑定积分',
  `ex_points` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '已兑换积分',
  `invite_points` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '邀请得积分',
  `total_points` int(11) NOT NULL DEFAULT '0' COMMENT '用户的所有历史积分',
  `sign_days` smallint(5) unsigned NOT NULL DEFAULT '0' COMMENT '签到天数',
  `invited_by` varchar(20) DEFAULT NULL COMMENT '邀请源',
  `invited_code` varchar(20) DEFAULT NULL COMMENT '邀请code',
  `invites` int(10) unsigned DEFAULT '0' COMMENT '总邀请人数',
  `locale` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `scopeid` (`scopeid`),
  UNIQUE KEY `invited_code` (`invited_code`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='账户信息' AUTO_INCREMENT=35 ;

-- --------------------------------------------------------

--
-- 表的结构 `user_bind`
--

CREATE TABLE IF NOT EXISTS `user_bind` (
  `userid` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  `token` varchar(64) DEFAULT NULL,
  `type` int(3) DEFAULT NULL COMMENT '0:facebook;1:gamil'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `user_device`
--

CREATE TABLE IF NOT EXISTS `user_device` (
  `uid` int(8) unsigned NOT NULL AUTO_INCREMENT,
  `ei` varchar(32) DEFAULT NULL,
  `si` varchar(32) DEFAULT NULL,
  `mac` char(12) DEFAULT NULL,
  `andid` varchar(32) DEFAULT NULL,
  `fingerprinting` varchar(64) DEFAULT NULL COMMENT '设备指纹',
  PRIMARY KEY (`uid`),
  KEY `fingerprinting` (`fingerprinting`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户帐号对应的设备' AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `user_sign`
--

CREATE TABLE IF NOT EXISTS `user_sign` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(8) unsigned NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
