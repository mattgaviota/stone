<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');


class Model_Log_Usuarios extends CI_Model {

    function __construct()
    {
        parent::__construct();
    }

    function all(){
    	$query = $this->db->get('log_usuarios');
    	return $query->result();
    }

    function find($fecha){
    	$this->db->where('fecha',$fecha);
    	return $this->db->get('log_usuarios');
    }

    //retorna el id
    function add_log($registro){
        $this->db->trans_start();
    	$this->db->set($registro);
    	$this->db->insert('log_usuarios');
        $insert_id = $this->db->insert_id();
        $this->db->trans_complete();
        return $insert_id;
    }

    function update($registro){
        $this->db->trans_start();
    	$this->db->set($registro);
    	$this->db->where('id',$registro['id']);
    	$this->db->update('log_usuarios');
        $this->db->trans_complete();
    }

    function delete($id){
        $this->db->trans_start();
    	$this->db->where('id',$id);
    	$this->db->delete('log_usuarios');
        $this->db->trans_complete();
    }

    function find_accion($nombre_canonico){
    	$this->db->where('nombre_canonico', $nombre_canonico);
    	return $this->db->get('acciones');
    }
}