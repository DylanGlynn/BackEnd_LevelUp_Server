UPDATE levelupapi_game SET type_id = 2 WHERE levelupapi_game.id = 2;
DELETE from levelupapi_event WHERE id > 3;

ALTER TABLE levelupapi_event RENAME COLUMN game TO game_id;

ALTER TABLE levelupapi_attendance RENAME TO 'event_gamer';
ALTER TABLE event_gamer RENAME TO 'levelupapi_attendance';