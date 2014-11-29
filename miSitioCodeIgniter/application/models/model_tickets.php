<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');


class Model_Tickets extends CI_Model {

    function __construct()
    {
        parent::__construct();
    }

    function all(){
    	$query = $this->db->get('tickets');
    	return $query->result();
    }

    function find($id){
    	$this->db->where('id',$id);
    	return $this->db->get('tickets')->row();
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
        $query = $this->db->query("SELECT dias.fecha,extract(day FROM dias.fecha) AS dia, tickets.id AS id_ticket,log_usuarios.dni FROM dias LEFT JOIN tickets ON dias.id = tickets.id_dia LEFT JOIN log_usuarios ON tickets.id_log_usuario = log_usuarios.id WHERE dni = '$dni' AND dias.fecha::text LIKE '$fecha' AND estado = 1");
        return $query->result();
    }

    //Obtener los 5 tickets próximos al día de hoy si los tiene.
    function get_tickets_proximos($dni){
        $query = $this->db->query("SELECT tabla.*,dias.fecha AS fecha_ticket FROM (SELECT * FROM tickets WHERE estado = 1) tabla LEFT JOIN dias ON tabla.id_dia = dias.id LEFT JOIN log_usuarios ON tabla.id_log_usuario = log_usuarios.id WHERE dni = '$dni' AND dias.fecha >= current_date ORDER BY dias.fecha LIMIT 5");
        return $query->result();
    }

}