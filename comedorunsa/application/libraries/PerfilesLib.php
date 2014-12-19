<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class PerfilesLib {

	function __construct(){
		$this->CI = & get_instance();//Obtener la instancia del objeto por referencia.
		$this->CI->load->model('Model_Perfiles');//Cargamos el modelo.
		$this->CI->load->model('Model_Perfiles_Tipos_Operaciones');
	}

	public function norepetir($registro){
		$this->CI->db->where('nombre', $registro['nombre']);
		$query = $this->CI->db->get('perfiles');
		if($query->num_rows() > 0 AND (!isset($registro['id']) OR ($registro['id'] != $query->row('id')))){
			return FALSE;
		}else{
			return TRUE;
		}
	}

	//Devolverá tanto las operaciones asignadas como las no asignadas
	public function get_operaciones($id_perfil){
		$lista_asignados = array();
		$lista_noasignados = array();

		$this->CI->load->model('Model_Tipos_Operaciones');
        $tipos_operaciones = $this->CI->Model_Tipos_Operaciones->all();

        foreach($tipos_operaciones as $tipo_operacion) {
            $this->CI->db->where('id_perfil', $id_perfil);
            $this->CI->db->where('id_tipo_operacion', $tipo_operacion->id);
            $query = $this->CI->db->get('perfiles_tipos_operaciones');
            $existe = ($query->num_rows >0);

            if($existe) {
                $lista_asignados[] = array($tipo_operacion->id, $tipo_operacion->nombre, $id_perfil);
            }else {
                $lista_noasignados[] = array($tipo_operacion->id, $tipo_operacion->nombre, $id_perfil);
            }
        }

		return array($lista_asignados, $lista_noasignados);
	}

	public function dar_permiso($id_tipo_operacion, $id_perfil){
		$registro = array();
		$registro['id_tipo_operacion'] = $id_tipo_operacion;
		$registro['id_perfil'] = $id_perfil;
		$registro['created'] = date('Y/m/d H:i');
		$registro['updated'] = date('Y/m/d H:i');
		$this->CI->Model_Perfiles_Tipos_Operaciones->insert($registro);
	}

	public function quitar_permiso($id_tipo_operacion, $id_perfil){
		$this->CI->db->where('id_perfil', $id_perfil);
		$this->CI->db->where('id_tipo_operacion', $id_tipo_operacion);
		$this->CI->db->delete('perfiles_tipos_operaciones');
	}

	public function findByTipoOperacionAndPerfil($id_tipo_operacion, $id_perfil){
	    $this->CI->db->where('id_perfil', $id_perfil);
        $this->CI->db->where('id_tipo_operacion', $id_tipo_operacion);
        return $this->CI->db->get('perfiles_tipos_operaciones')->row();
	}

}