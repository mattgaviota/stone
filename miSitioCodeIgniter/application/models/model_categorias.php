<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');


class Model_Categorias extends CI_Model {

    function __construct()
    {
        parent::__construct();
    }

    function all(){
    	$query = $this->db->get('categorias');
    	return $query->result();
    }

    function allFilter($campo, $valor){
        $this->db->like($campo, $valor);
        $query = $this->db->get('categorias');
        return $query->result();
    }

    function find($id){
    	$this->db->where('id',$id);
    	return $this->db->get('categorias')->row();
    }

    function findNombre($nombre){
        $this->db->where('nombre',$nombre);
        return $this->db->get('categorias')->row();   
    }

    function insert($registro){
    	$this->db->set($registro);
    	$this->db->insert('categorias');
    }

    function update($registro){
    	$this->db->set($registro);
    	$this->db->where('id',$registro['id']);
    	$this->db->update('categorias');
    }

    function delete($id){
    	$this->db->where('id',$id);
    	$this->db->delete('categorias');
    }

}