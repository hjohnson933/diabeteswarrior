SELECT DISTINCT foods.index, foods.ts, users.username, foods.domain, foods.name, foods.portion, units.v, foods.calories, foods.fat, foods.cholesterol, foods.sodium, foods.carbohydrate, foods.protein FROM foods LEFT JOIN users on foods.user_id = users.id LEFT JOIN units on foods.unit = units.k WHERE foods.user_id = users.id AND foods.unit = units.k ORDER BY foods.index;