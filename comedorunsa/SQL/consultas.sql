select dias.*, tickets.id as id_ticket,log_usuarios.dni from dias 
left join tickets on dias.id = tickets.id_dia left join log_usuarios on tickets.id_log_usuario = log_usuarios.id 
where dni = '33661787' and dias.fecha::text LIKE '2014-11%';

select tickets.id, dias.fecha, log_usuarios.dni from tickets join
dias on tickets.id_dia = dias.id join log_usuarios on tickets.id_log_usuario = log_usuarios.id
where dias.fecha = '2014-11-05' and dni = '33661787'

select facultades.nombre, count(usuarios.id_facultad) from facultades left join usuarios on facultades.id = usuarios.id_facultad group by facultades.nombre;

select categorias.nombre, count(usuarios.id_categoria) from categorias left join usuarios on categorias.id = usuarios.id_categoria group by categorias.nombre;

SELECT facultades.nombre, count(usuarios.id_facultad) as total_usuarios,
    count(CASE WHEN id_categoria = 1 THEN 1 END) as becado,
    count(CASE WHEN id_categoria = 2 THEN 1 END) as regulares,
    count(CASE WHEN id_categoria = 3 THEN 1 END) as gratuito
FROM
   facultades
LEFT JOIN 
	usuarios ON facultades.id = usuarios.id_facultad GROUP BY facultades.nombre;

select facultades.nombre, categorias.nombre, count(*) as Cantidad_de_Tickets, sum(tickets.importe) as Total from tickets
	left join log_usuarios on log_usuarios.id = tickets.id_log_usuario
	left join usuarios on log_usuarios.dni = usuarios.dni
	left join facultades on usuarios.id_facultad = facultades.id
	left join categorias on usuarios.id_categoria = categorias.id
	where tickets.estado <> 0
	group by facultades.nombre, categorias.nombre;

select facultades.nombre, count(tabla.id_tickets) from facultades left join
(select tickets.id as id_tickets, log_usuarios.id, dias.fecha,id_facultad, usuarios.nombre from tickets 
inner join dias on tickets.id_dia = dias.id
inner join log_usuarios on tickets.id_log_usuario = log_usuarios.id
inner join usuarios on log_usuarios.dni = usuarios.dni
where tickets.estado = 1 and log_usuarios.id_accion = 1) as tabla on
tabla.id_facultad = facultades.id
group by facultades.nombre;


select facultades.nombre, count(tabla.id_tickets)as total_tickets, 
count(CASE WHEN id_categoria = 1 THEN 1 END) as becado,
count(CASE WHEN id_categoria = 2 THEN 1 END) as regulares,
count(CASE WHEN id_categoria = 3 THEN 1 END) as gratuito,
coalesce(sum(tabla.importe),0) as total_pesos
from facultades left join
(select tickets.id as id_tickets,id_facultad, id_categoria,tickets.importe as importe from tickets 
inner join dias on tickets.id_dia = dias.id
inner join log_usuarios on tickets.id_log_usuario = log_usuarios.id
inner join usuarios on log_usuarios.dni = usuarios.dni
where tickets.estado = 1 and log_usuarios.id_accion = 1) as tabla on
tabla.id_facultad = facultades.id
group by facultades.nombre;

select facultades.nombre, count(tabla.id_tickets)as total_tickets, 
count(CASE WHEN id_categoria = 1 THEN 1 END) as becado,
count(CASE WHEN id_categoria = 2 THEN 1 END) as regulares,
count(CASE WHEN id_categoria = 3 THEN 1 END) as gratuito,
coalesce(sum(tabla.importe),0) as total_pesos
from facultades left join
(select tickets.id as id_tickets,id_facultad, id_categoria,tickets.importe as importe from tickets 
inner join dias on tickets.id_dia = dias.id
inner join log_usuarios on tickets.id_log_usuario = log_usuarios.id
inner join usuarios on log_usuarios.dni = usuarios.dni
where tickets.estado = 1 and log_usuarios.id_accion = 1 and dias.fecha = '2014-11-27') as tabla on
tabla.id_facultad = facultades.id
group by facultades.nombre;

SELECT COUNT(tickets.id) AS total_tickets, 
COUNT(CASE WHEN id_categoria = 1 THEN 1 END) AS becados, 
COUNT(CASE WHEN id_categoria = 2 THEN 1 END) AS regulares, 
COUNT(CASE WHEN id_categoria = 3 THEN 1 END) AS gratuitos,
SUM(tickets.importe) FROM tickets
inner join dias on tickets.id_dia = dias.id
inner join log_usuarios on tickets.id_log_usuario = log_usuarios.id
inner join usuarios on log_usuarios.dni = usuarios.dni
where tickets.estado = 2 and dias.fecha between '2014-12-3' and '2014-12-3';

select facultades.nombre, count(tabla.id_tickets) as total_tickets, 
count(CASE WHEN estado = 0 THEN 1 END) as anulados,
count(CASE WHEN estado = 1 THEN 1 END) as activos,
count(CASE WHEN estado = 2 THEN 1 END) as impresos,
count(CASE WHEN estado = 3 THEN 1 END) as consumidos
from facultades left join
(select tickets.id as id_tickets,id_facultad, id_categoria,tickets.estado as estado from tickets 
inner join dias on tickets.id_dia = dias.id
inner join log_usuarios on tickets.id_log_usuario = log_usuarios.id
inner join usuarios on log_usuarios.dni = usuarios.dni) as tabla on
tabla.id_facultad = facultades.id
group by facultades.nombre;

SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'comedorDB';

select tickets.id, dias.fecha, tickets.importe as importe,estados_tickets.nombre, usuarios.dni, usuarios.nombre
from tickets
inner join dias on tickets.id_dia = dias.id
inner join estados_tickets on tickets.estado = estados_tickets.id
inner join (select distinct on(id_ticket) id_ticket, id, id_log_usuario from tickets_log_usuarios) as tickets_log_usuarios
on tickets.id = tickets_log_usuarios.id_ticket
inner join log_usuarios on tickets_log_usuarios.id_log_usuario = log_usuarios.id
inner join usuarios on usuarios.dni = log_usuarios.dni
order by dias.fecha desc;

select id_ticket, log_usuarios.id as id_log,log_usuarios.fecha as fecha, acciones.nombre as accion, log_usuarios.lugar as lugar
from tickets_log_usuarios 
inner join log_usuarios on tickets_log_usuarios.id_log_usuario = log_usuarios.id
inner join acciones on log_usuarios.id_accion = acciones.id
where id_ticket = 180 order by id_log_usuario;

SELECT dias.fecha AS Dias,
COUNT(tabla.id_tickets) AS total_tickets,
COUNT(CASE WHEN id_categoria = 1 THEN 1 END) AS becados,
COUNT(CASE WHEN id_categoria = 2 THEN 1 END) AS regulares,
COUNT(CASE WHEN id_categoria = 3 THEN 1 END) AS gratuitos,
COALESCE(SUM(tabla.importe),0) AS total_pesos FROM dias
LEFT JOIN (SELECT tickets.id_dia AS id_dia,tickets.id AS id_tickets,id_facultad, id_categoria,tickets.importe AS importe
FROM tickets
INNER JOIN  tickets_log_usuarios ON tickets.id = tickets_log_usuarios.id_ticket
INNER JOIN log_usuarios ON log_usuarios.id = tickets_log_usuarios.id_log_usuario
INNER JOIN usuarios ON log_usuarios.dni = usuarios.dni 
WHERE tickets.estado <> 0) AS tabla 
ON tabla.id_dia = dias.id GROUP BY dias.fecha
ORDER BY dias.fecha;


SELECT dias.fecha AS Dias,
COUNT(tabla.id_tickets) AS total_tickets,
COUNT(CASE WHEN id_categoria = 1 THEN 1 END) AS becados,
COUNT(CASE WHEN id_categoria = 2 THEN 1 END) AS regulares,
COUNT(CASE WHEN id_categoria = 3 THEN 1 END) AS gratuitos,
COALESCE(SUM(CASE WHEN id_categoria = 1 THEN tabla.importe END),0) AS subtotal_becados,
COALESCE(SUM(CASE WHEN id_categoria = 2 THEN tabla.importe END),0) AS subtotal_regulares,
COALESCE(SUM(CASE WHEN id_categoria = 3 THEN tabla.importe END),0) AS subtotal_gratuitos,
COALESCE(SUM(tabla.importe),0) AS total_tickets FROM dias
LEFT JOIN (SELECT tickets.id_dia AS id_dia,tickets.id AS id_tickets,id_facultad, id_categoria,tickets.importe AS importe
FROM tickets
INNER JOIN (SELECT distinct on(id_ticket) id_ticket, id_log_usuario FROM tickets_log_usuarios) AS tickets_log_usuarios ON tickets.id = tickets_log_usuarios.id_ticket
INNER JOIN log_usuarios ON log_usuarios.id = tickets_log_usuarios.id_log_usuario
INNER JOIN usuarios ON log_usuarios.dni = usuarios.dni 
WHERE tickets.estado <> 0) AS tabla 
ON tabla.id_dia = dias.id GROUP BY dias.fecha
ORDER BY dias.fecha;
