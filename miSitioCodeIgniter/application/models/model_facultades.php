<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');


class Model_Facultades extends CI_Model {

    function __construct()
    {
        parent::__construct();
    }

    function all(){
    	$query = $this->db->get('facultades');
    	return $query->result();
    }

    function allFilter($campo, $valor){
        $this->db->like($campo, $valor);
        $query = $this->db->get('facultades');
        return $query->result();
    }

    function find($id){
    	$this->db->where('id',$id);
    	return $this->db->get('facultades')->row();
    }

    function findNombre($nombre){
        $this->db->where('nombre',$nombre);
        return $this->db->get('facultades');   
    }

    function insert($registro){
    	$this->db->set($registro);
    	$this->db->insert('facultades');
    }

    function update($registro){
    	$this->db->set($registro);
    	$this->db->where('id',$registro['id']);
    	$this->db->update('facultades');
    }

    function delete($id){
    	$this->db->where('id',$id);
    	$this->db->delete('facultades');
    }

    function clasificacion_usuarios(){
        $query = $this->db->query("SELECT facultades.nombre AS facultad, COUNT(usuarios.id_facultad) AS total_usuarios, COUNT(CASE WHEN id_categoria = 1 THEN 1 END) AS becados, COUNT(CASE WHEN id_categoria = 2 THEN 1 END) AS regulares, COUNT(CASE WHEN id_categoria = 3 THEN 1 END) AS gratuitos FROM facultades LEFT JOIN usuarios ON facultades.id = usuarios.id_facultad GROUP BY facultades.nombre");
        return $query->result();
    }
}
