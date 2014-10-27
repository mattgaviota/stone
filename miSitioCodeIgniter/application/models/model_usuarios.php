<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');


class Model_Usuarios extends CI_Model {

    function __construct()
    {
        parent::__construct();
    }

    function all(){
        $this->db->select('usuarios.*, perfiles.nombre as perfil_nombre');
        $this->db->from('usuarios');
        $this->db->join('perfiles', 'usuarios.id_perfil = perfiles.id', 'left');

    	$query = $this->db->get();//Equivale a SELECT * FROM usuarios
    	return $query->result();//Devuelve un array asociativo.
    }

    function allRecargado(){
        $this->db->select('usuarios.*, perfiles.nombre as perfil_nombre, provincias.nombre as provincia_nombre, facultades.nombre as facultad_nombre, categorias.nombre as categoria_nombre');
        $this->db->from('usuarios');
        $this->db->join('perfiles', 'usuarios.id_perfil = perfiles.id', 'left');
        $this->db->join('provincias', 'usuarios.id_provincia = provincias.id', 'left');
        $this->db->join('facultades', 'usuarios.id_facultad = facultades.id', 'left');
        $this->db->join('categorias', 'usuarios.id_categoria = categorias.id', 'left');
        $query = $this->db->get();
        return $query->result();
    }

    function allFilter($campo, $valor){
        $this->db->select('usuarios.*, perfiles.nombre as perfil_nombre');
        $this->db->from('usuarios');
        $this->db->join('perfiles', 'usuarios.id_perfil = perfiles.id', 'left');
        $this->db->like($campo,$valor);

        $query = $this->db->get();
        return $query->result();
    }

    function find($dni){
        $this->db->select('usuarios.*, perfiles.nombre as perfil_nombre, provincias.nombre as provincia_nombre, facultades.nombre as facultad_nombre, categorias.nombre as categoria_nombre');
        $this->db->from('usuarios');
        $this->db->join('perfiles', 'usuarios.id_perfil = perfiles.id', 'left');
        $this->db->join('provincias', 'usuarios.id_provincia = provincias.id', 'left');
        $this->db->join('facultades', 'usuarios.id_facultad = facultades.id', 'left');
        $this->db->join('categorias', 'usuarios.id_categoria = categorias.id', 'left');

    	$this->db->where('usuarios.dni',$dni);
    	return $this->db->get()->row();//Equivale a SELECT * FROM usuarios WHERE id='$id'
    }

    function insert($registro){
    	$this->db->set($registro);
    	$this->db->insert('usuarios');
    }

    function update($registro){
    	$this->db->set($registro);
    	$this->db->where('dni',$registro['dni']);
    	$this->db->update('usuarios');
    }

    function delete($dni){
    	$this->db->where('dni',$dni);
    	$this->db->delete('usuarios');
    }

    function get_login($dni){
    	$this->db->where('dni',$dni);//El dni es el login de usuario
    	return $this->db->get('usuarios');//SELECT * FROM usuarios WHERE () and ()
    }

    function get_perfiles(){
        $lista = array();
        $this->load->model('Model_Perfiles');
        $registros = $this->Model_Perfiles->all();

        foreach($registros as $registro){
            $lista[$registro->id] = $registro->nombre;
        }
        return $lista;
    }

    function get_provincias(){
        $lista = array();
        $this->load->model('Model_Provincias');
        $registros = $this->Model_Provincias->all();
        foreach($registros as $registro){
            $lista[$registro->id] = $registro->nombre;
        }
        return $lista;
    }

    function get_facultades(){
        $lista = array();
        $this->load->model('Model_Facultades');
        $registros = $this->Model_Facultades->all();
        foreach($registros as $registro){
            $lista[$registro->id] = $registro->nombre;
        }
        return $lista;
    }

    function get_categorias(){
        $lista = array();
        $registros = $this->db->get('categorias')->result();
        foreach($registros as $registro){
            $lista[$registro->id] = $registro->nombre;
        }
        return $lista;
    }

    function get_ultimas_operaciones($dni){
        $this->db->select('log_usuarios.*, acciones.nombre as nombre_accion');
        $this->db->from('log_usuarios');
        $this->db->join('acciones', 'log_usuarios.id_accion = acciones.id', 'left');
        $this->db->where('dni', $dni);
        $this->db->order_by('fecha','desc');
        $this->db->limit(5);
        return $query = $this->db->get()->row();
    }
}