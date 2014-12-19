<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');


class Model_Tickets extends CI_Model {

    function __construct()
    {
        parent::__construct();
    }

    function all(){
        $query = $this->db->query('SELECT tickets.id AS id_ticket, dias.fecha AS fecha, tickets.importe AS importe_ticket, estados_tickets.nombre AS estado_ticket, usuarios.dni AS dni, usuarios.nombre AS nombre_usuario
                FROM tickets
                INNER JOIN dias ON tickets.id_dia = dias.id
                INNER JOIN estados_tickets on tickets.estado = estados_tickets.id
                inner join 
                    (SELECT DISTINCT ON(id_ticket) id_ticket, id_log_usuario FROM tickets_log_usuarios) AS tickets_log_usuarios 
                ON tickets_log_usuarios.id_ticket = tickets.id
                INNER JOIN log_usuarios ON tickets_log_usuarios.id_log_usuario = log_usuarios.id
                INNER JOIN usuarios ON log_usuarios.dni = usuarios.dni
                ORDER BY dias.fecha DESC');
        return $query->result();
    }

    function all_filter($buscar_nombre,$buscar_dni, $buscar_id, $buscar_fecha){
        if($buscar_fecha === ''){            
            $query = $this->db->query("SELECT tickets.id AS id_ticket, dias.fecha AS fecha, tickets.importe AS importe_ticket, estados_tickets.nombre AS estado_ticket, usuarios.dni AS dni, usuarios.nombre AS nombre_usuario
                    FROM tickets
                    INNER JOIN dias ON tickets.id_dia = dias.id
                    INNER JOIN estados_tickets on tickets.estado = estados_tickets.id
                    inner join 
                        (SELECT DISTINCT ON(id_ticket) id_ticket, id_log_usuario FROM tickets_log_usuarios) AS tickets_log_usuarios 
                    ON tickets_log_usuarios.id_ticket = tickets.id
                    INNER JOIN log_usuarios ON tickets_log_usuarios.id_log_usuario = log_usuarios.id
                    INNER JOIN usuarios ON log_usuarios.dni = usuarios.dni
                    WHERE LOWER(usuarios.nombre) LIKE '%{$buscar_nombre}%' AND
                    usuarios.dni LIKE '{$buscar_dni}%' AND
                    tickets.id::text LIKE '{$buscar_id}%'
                    ORDER BY dias.fecha DESC");
        }else{
            $query = $this->db->query("SELECT tickets.id AS id_ticket, dias.fecha AS fecha, tickets.importe AS importe_ticket, estados_tickets.nombre AS estado_ticket, usuarios.dni AS dni, usuarios.nombre AS nombre_usuario
                    FROM tickets
                    INNER JOIN dias ON tickets.id_dia = dias.id
                    INNER JOIN estados_tickets on tickets.estado = estados_tickets.id
                    inner join 
                        (SELECT DISTINCT ON(id_ticket) id_ticket, id_log_usuario FROM tickets_log_usuarios) AS tickets_log_usuarios 
                    ON tickets_log_usuarios.id_ticket = tickets.id
                    INNER JOIN log_usuarios ON tickets_log_usuarios.id_log_usuario = log_usuarios.id
                    INNER JOIN usuarios ON log_usuarios.dni = usuarios.dni
                    WHERE LOWER(usuarios.nombre) LIKE '%{$buscar_nombre}%' AND
                    usuarios.dni LIKE '{$buscar_dni}%' AND
                    tickets.id::text LIKE '{$buscar_id}%' AND dias.fecha = '$buscar_fecha'
                    ORDER BY dias.fecha DESC");            
        }
        return $query->result();
    }

    function find($id){
        $this->db->where('id',$id);
        return $this->db->get('tickets')->row();
    }

    function get_ticket_detalle($id_ticket){
        $this->db->select('id_ticket, log_usuarios.id as id_log,log_usuarios.fecha as fecha, acciones.nombre as accion, log_usuarios.lugar as lugar');
        $this->db->from('tickets_log_usuarios');
        $this->db->join('log_usuarios', 'log_usuarios.id = tickets_log_usuarios.id_log_usuario');
        $this->db->join('acciones', 'acciones.id = log_usuarios.id_accion');
        $this->db->where('id_ticket', $id_ticket);
        $this->db->order_by('id_log_usuario', 'asc');
        $query = $this->db->get();
        return $query->result();
    }

    function add_ticket($registro){
        $this->db->trans_start();
        $this->db->set($registro);
        $this->db->insert('tickets');
        $insert_id = $this->db->insert_id();
        $this->db->trans_complete();
        return $insert_id;
    }

    function update($registro){
        $this->db->trans_start();
        $this->db->set($registro);
        $this->db->where('id',$registro['id']);
        $this->db->update('tickets');
        $this->db->trans_complete();
    }

    function delete($id){
        $this->db->where('id',$id);
        $this->db->delete('tickets');
    }

    //Devuelve todos los días para los que el usuario tiene ticket.
    function get_dias_tickets($fecha, $dni){
        $query = $this->db->query("SELECT dias.fecha,extract(day FROM dias.fecha) AS dia, tickets.id AS id_ticket,log_usuarios.dni FROM dias LEFT JOIN tickets ON dias.id = tickets.id_dia LEFT JOIN tickets_log_usuarios ON tickets.id = tickets_log_usuarios.id_ticket LEFT JOIN log_usuarios ON log_usuarios.id = tickets_log_usuarios.id_log_usuario WHERE dni = '$dni' AND dias.fecha::text LIKE '$fecha' AND estado = 1");
        return $query->result();
    }

    //Obtener los 5 tickets próximos al día de hoy si los tiene.
    function get_tickets_proximos($dni){
        $query = $this->db->query("SELECT tabla.*,dias.fecha AS fecha_ticket FROM (SELECT * FROM tickets WHERE estado = 1) tabla LEFT JOIN dias ON tabla.id_dia = dias.id LEFT JOIN tickets_log_usuarios ON tabla.id = tickets_log_usuarios.id_ticket LEFT JOIN log_usuarios ON log_usuarios.id = tickets_log_usuarios.id_log_usuario WHERE dni = '$dni' AND dias.fecha >= current_date ORDER BY dias.fecha LIMIT 5");
        return $query->result();
    }

    function servicios_tickets($desde, $hasta){
        $query = $this->db->query("SELECT facultades.nombre AS facultad,
            COUNT(tabla.id_tickets) AS total_tickets,
            COUNT(CASE WHEN id_categoria = 1 THEN 1 END) AS becados,
            COUNT(CASE WHEN id_categoria = 2 THEN 1 END) AS regulares,
            COUNT(CASE WHEN id_categoria = 3 THEN 1 END) AS gratuitos,
            COALESCE(SUM(tabla.importe),0) AS total_pesos FROM facultades
            LEFT JOIN (SELECT tickets.id AS id_tickets,id_facultad, id_categoria,tickets.importe AS importe
                FROM tickets INNER JOIN dias ON tickets.id_dia = dias.id
                INNER JOIN  tickets_log_usuarios ON tickets.id = tickets_log_usuarios.id_ticket
                INNER JOIN log_usuarios ON log_usuarios.id = tickets_log_usuarios.id_log_usuario
                INNER JOIN usuarios ON log_usuarios.dni = usuarios.dni
                WHERE tickets.estado <> 0 AND dias.fecha BETWEEN '$desde' AND '$hasta') AS tabla ON tabla.id_facultad = facultades.id GROUP BY facultades.nombre");

        return $query->result();
    }

    function get_total_servicios($desde, $hasta){
        $query = $this->db->query("SELECT COUNT(tickets.id) AS total_tickets,
            COUNT(CASE WHEN id_categoria = 1 THEN 1 END) AS becados,
            COUNT(CASE WHEN id_categoria = 2 THEN 1 END) AS regulares,
            COUNT(CASE WHEN id_categoria = 3 THEN 1 END) AS gratuitos,
            COALESCE(SUM(tickets.importe),0) AS total_importe FROM tickets
            INNER JOIN dias ON tickets.id_dia = dias.id
            INNER JOIN (SELECT distinct on(id_ticket) id_ticket, id_log_usuario FROM tickets_log_usuarios) AS tickets_log_usuarios ON tickets.id = tickets_log_usuarios.id_ticket
            INNER JOIN log_usuarios ON log_usuarios.id = tickets_log_usuarios.id_log_usuario
            INNER JOIN usuarios ON log_usuarios.dni = usuarios.dni
            WHERE tickets.estado <> 0 AND dias.fecha BETWEEN '$desde' AND '$hasta'");
        return $query;
    }

    function clasificacion_tickets($desde, $hasta){
        $query = $this->db->query("SELECT facultades.nombre AS facultad, 
            COUNT(tabla.id_tickets) as total_tickets,
            COUNT(CASE WHEN estado = 0 THEN 1 END) as anulados,
            COUNT(CASE WHEN estado = 1 THEN 1 END) as activos,
            COUNT(CASE WHEN estado = 2 THEN 1 END) as impresos,
            COUNT(CASE WHEN estado = 3 THEN 1 END) as consumidos 
            FROM facultades LEFT JOIN
                (SELECT tickets.id AS id_tickets,id_facultad, id_categoria,tickets.estado AS estado 
                    FROM tickets INNER JOIN dias ON tickets.id_dia = dias.id 
                    INNER JOIN (SELECT distinct on(id_ticket) id_ticket, id_log_usuario FROM tickets_log_usuarios) AS tickets_log_usuarios ON tickets.id = tickets_log_usuarios.id_ticket
                    INNER JOIN log_usuarios ON log_usuarios.id = tickets_log_usuarios.id_log_usuario
                    INNER JOIN usuarios ON log_usuarios.dni = usuarios.dni
                    WHERE dias.fecha BETWEEN '$desde' AND '$hasta') AS tabla 
                    ON tabla.id_facultad = facultades.id 
                    GROUP BY facultades.nombre");
        return $query->result();
    }

    function get_total_tickets($desde, $hasta){
        $query = $this->db->query("SELECT COUNT(tickets.id) AS total_tickets,
                COUNT(CASE WHEN tickets.estado = 0 THEN 1 END) AS anulados,
                COUNT(CASE WHEN tickets.estado = 1 THEN 1 END) AS activos,
                COUNT(CASE WHEN tickets.estado = 2 THEN 1 END) AS impresos,
                COUNT(CASE WHEN tickets.estado = 3 THEN 1 END) AS consumidos
                FROM tickets INNER JOIN dias ON tickets.id_dia = dias.id
                INNER JOIN (SELECT distinct on(id_ticket) id_ticket, id_log_usuario FROM tickets_log_usuarios) AS tickets_log_usuarios ON tickets.id = tickets_log_usuarios.id_ticket
                INNER JOIN log_usuarios ON log_usuarios.id = tickets_log_usuarios.id_log_usuario
                INNER JOIN usuarios ON log_usuarios.dni = usuarios.dni
                WHERE dias.fecha BETWEEN '$desde' AND '$hasta'");
        return $query;
    }


}