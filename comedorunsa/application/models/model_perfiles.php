<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');


class Model_Perfiles extends CI_Model {

    function __construct()
    {
        parent::__construct();
    }

    function all(){
    	$query = $this->db->get('perfiles');
    	return $query->result();
    }

    function allFilter($campo, $valor){
        $this->db->like($campo, $valor);
        $query = $this->db->get('perfiles');
        return $query->result();
    }

    function find($id){
    	$this->db->where('id',$id);
    	return $this->db->get('perfiles')->row();
    }

    function findNombre($nombre){
        $this->db->where('nombre',$nombre);
        return $this->db->get('perfiles')->row();   
    }

    function insert($registro){
    	$this->db->set($registro);
    	$this->db->insert('perfiles');
    }

    function update($registro){
    	$this->db->set($registro);
    	$this->db->where('id',$registro['id']);
    	$this->db->update('perfiles');
    }

    function delete($id){
    	$this->db->where('id',$id);
    	$this->db->delete('perfiles');
    }

}