<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');


class Model_Log_Usuarios extends CI_Model {

    function __construct()
    {
        parent::__construct();
    }

    function all(){
        $this->db->select('log_usuarios.*, acciones.nombre as accion');
        $this->db->from('log_usuarios');
        $this->db->join('acciones', 'log_usuarios.id_accion = acciones.id');
        $this->db->order_by('fecha', 'desc');
    	$query = $this->db->get();
    	return $query->result();
    }

    function all_filter($accion, $buscar_dni){
        if($accion == '0'){
            $this->db->select('log_usuarios.*, acciones.nombre as accion');
            $this->db->from('log_usuarios');
            $this->db->join('acciones', 'log_usuarios.id_accion = acciones.id');
            $this->db->like('dni', $buscar_dni, 'after');
            $this->db->order_by('fecha', 'desc');
            $query = $this->db->get();
            return $query->result();
        }else{
            $this->db->select('log_usuarios.*, acciones.nombre as accion');
            $this->db->from('log_usuarios');
            $this->db->join('acciones', 'log_usuarios.id_accion = acciones.id');
            $this->db->where('id_accion', $accion);
            $this->db->like('dni', $buscar_dni, 'after');
            $this->db->order_by('fecha', 'desc');
            $query = $this->db->get();
            return $query->result();            
        }
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

    function get_acciones(){
        $lista = array();
        $registros = $this->db->get('acciones')->result();
        $lista[0] = 'Todos';
        foreach($registros as $registro){
            $lista[$registro->id] = $registro->nombre;
        }
        return $lista;
    }
}