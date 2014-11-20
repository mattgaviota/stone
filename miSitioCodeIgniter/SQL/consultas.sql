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
count(CASE WHEN id_categoria = 3 THEN 1 END) as gratuito 
from facultades left join
(select tickets.id as id_tickets,id_facultad, id_categoria from tickets 
inner join dias on tickets.id_dia = dias.id
inner join log_usuarios on tickets.id_log_usuario = log_usuarios.id
inner join usuarios on log_usuarios.dni = usuarios.dni
where tickets.estado = 1 and log_usuarios.id_accion = 1) as tabla on
tabla.id_facultad = facultades.id
group by facultades.nombre
