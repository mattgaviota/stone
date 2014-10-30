<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');


class Model_Configuraciones extends CI_Model {

    function __construct()
    {
        parent::__construct();
    }

    function all(){
    	$query = $this->db->get('configuraciones');
    	return $query->result();
    }
    
    function find($id){
    	$this->db->where('id',$id);
    	return $this->db->get('configuraciones')->row();
    }

    function insert($registro){
    	$this->db->set($registro);
    	$this->db->insert('configuraciones');
    }

    function update($registro){
    	$this->db->set($registro);
    	$this->db->where('id',$registro['id']);
    	$this->db->update('configuraciones');
    }

    function delete($id){
    	$this->db->where('id',$id);
    	$this->db->delete('configuraciones');
    }

}