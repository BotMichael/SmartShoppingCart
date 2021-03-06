DROP DATABASE IF EXISTS `smart_shopping_cart`;
CREATE DATABASE `smart_shopping_cart`;
USE `smart_shopping_cart`;

CREATE TABLE `user`(
		`phone` varchar(255) NOT NULL,
		`password` varchar(255) NOT NULL,
	PRIMARY KEY (`phone`)
);


CREATE TABLE `item`(
                `item` varchar(255) NOT NULL,
                `region` varchar(255) NOT NULL,
				`price` float NOT NULL,
        PRIMARY KEY (`item`)
);



CREATE TABLE `shopping_history`(
		`historyID` integer NOT NULL auto_increment,
		`time` timestamp NOT NULL DEFAULT now(),
		`user_phone` varchar(255),
		`item` varchar(255) NOT NULL,
		`num` integer NOT NULL,
	PRIMARY KEY (`historyID`),
	FOREIGN KEY (`item`) REFERENCES item(`item`)
);



insert into user values ('9495278828', '123');
insert into user values ('123', '123');

insert into item values ('water', 'A', 0.97);
insert into item values ('icecream', 'X', 4.9);
insert into item values ('apple', 'G', 1.0);
insert into item values ('orange', 'G', 4.99);
insert into item values ('milk tea', 'Y', 6.75);
insert into item values ('bottle', 'AA', 0.97);
insert into item values ('banana', 'G', 1.47);
insert into item values ('potted plant', 'L', 3.99);
insert into item values ('pineapple', 'L', 3.99);

INSERT INTO shopping_history (`user_phone`, `item`, `num`) VALUES (Null, 'icecream', 4);
INSERT INTO shopping_history (`user_phone`, `item`, `num`) VALUES (Null, 'icecream', 4);
INSERT INTO shopping_history (`user_phone`, `item`, `num`) VALUES (Null, 'icecream', 4);
INSERT INTO shopping_history (`user_phone`, `item`, `num`) VALUES (Null, 'icecream', 4);
INSERT INTO shopping_history (`user_phone`, `item`, `num`) VALUES (Null, 'icecream', 4);

INSERT INTO shopping_history (`time`, `user_phone`, `item`, `num`) VALUES ('2020-06-03 01:53:55', Null, 'apple', 4);
INSERT INTO shopping_history (`time`, `user_phone`, `item`, `num`) VALUES ('2020-06-03 01:53:55', Null, 'apple', 4);
INSERT INTO shopping_history (`time`, `user_phone`, `item`, `num`) VALUES ('2020-06-03 01:53:55', Null, 'apple', 4);
INSERT INTO shopping_history (`time`, `user_phone`, `item`, `num`) VALUES ('2020-06-03 01:53:55', Null, 'apple', 4);

INSERT INTO shopping_history (`time`, `user_phone`, `item`, `num`) VALUES ('2020-06-05 01:53:55', Null, 'bottle', 4);
INSERT INTO shopping_history (`time`, `user_phone`, `item`, `num`) VALUES ('2020-06-05 01:53:55', Null, 'bottle', 4);


