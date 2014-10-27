<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');


class Model_Provincias extends CI_Model {

    function __construct()
    {
        parent::__construct();
    }

    function all(){
    	$query = $this->db->get('provincias');
    	return $query->result();
    }

    function allFilter($campo, $valor){
        $this->db->like($campo, $valor);
        $query = $this->db->get('provincias');
        return $query->result();
    }

    function find($id){
    	$this->db->where('id',$id);
    	return $this->db->get('provincias')->row();
    }

    function findNombre($nombre){
        $this->db->where('nombre',$nombre);
        return $this->db->get('provincias');   
    }

    function insert($registro){
    	$this->db->set($registro);
    	$this->db->insert('provincias');
    }

    function update($registro){
    	$this->db->set($registro);
    	$this->db->where('id',$registro['id']);
    	$this->db->update('provincias');
    }

    function delete($id){
    	$this->db->where('id',$id);
    	$this->db->delete('provincias');
    }

    function get_provincias($buscar){
        //"SELECT * FROM tlocalidades WHERE snombrelocalidad LIKE '".$q."%'";
        $this->db->like('nombre', $buscar, 'after');
        $query = $this->db->get('provincias');
        return $query->result();
    }

    

}