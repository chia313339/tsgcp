CREATE TABLE simple_message_board (
	no serial PRIMARY KEY,
	name text,
	message text,
	datetime date,
	del_flg int

);

CREATE TABLE testimonials (
	no serial PRIMARY KEY,
	name text,
	title text,
	context text,
	pic_url text,
	del_flg int

);


CREATE TABLE food_order_setting (
	no serial PRIMARY KEY,
	order_no bigint, 
	order_store_no bigint, 
	order_owner text, 
	order_deadline timestamp, 
	order_remark text, 
	update_time date, 
	del_flg int
);

create table food_order(
	no serial PRIMARY KEY,
	order_no bigint, 
	 store_no bigint, 
	 order_name text, 
	 item_name text, 
	 item_price bigint, 
	 item_num bigint, 
	 item_remark text, 
	 update_time date, 
	 del_flg int, 
	 paid_flg int
);
 

 create table food_store_menu(
	no serial PRIMARY KEY,
	store_no bigint, 
	store_name text, 
	store_class text, 
	store_add text, 
	store_tel text, 
	pic_file text, 
	store_remark text,   
	store_menu text, 
	star int, 
	order_times date, 
	update_time date, 
	del_flg int
);