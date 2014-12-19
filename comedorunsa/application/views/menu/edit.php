<?= form_open('index.php/menu/update', array('class'=>'form-horizontal jumbotron')); ?>
	<legend>Editando un Registro</legend>

	<?= my_validation_errors(validation_errors()); ?>
	
	<div class="row">
		<div class="form-group">
			<?= form_label('ID: ', 'id', array('class'=>'col-sm-2 control-label')); ?>
			<div class="col-sm-4">
				<input type="text" name="id" value="<?= $registro->id; ?>" disabled/>
				<?= form_hidden('id', $registro->id); ?>
			</div>
		</div>
	</div>

	<div class="row">
		<div class="form-group">
			<?= form_label('Nombre: ', 'nombre', array('class'=>'col-sm-2 control-label')); ?>
			<div class="col-sm-4">
				<?= form_input(array('type'=>'text', 'name'=>'nombre', 'id'=>'nombre','value'=>$registro->nombre)); ?>
			</div>
		</div>
	</div>

	<div class="row">
		<div class="form-group">
			<?= form_label('Orden: ', 'orden', array('class'=>'col-sm-2 control-label')); ?>
			<div class="col-sm-4">
				<?= form_input(array('type'=>'number', 'name'=>'orden', 'id'=>'orden','value'=>$registro->orden)); ?>
			</div>
		</div>	
	</div>

	<div class="row">
		<div class="form-group">
			<?= form_label('Creado: ', 'created', array('class'=>'col-sm-2 control-label')); ?>
			<div class="col-sm-4">
				<input type="text" name="created" value="<?= date("d/m/Y - H:i",strtotime($registro->created)); ?>" disabled/>
				<?= form_hidden('created', $registro->created); ?>
			</div>
		</div>
	</div>


	<div class="form-group">
		<?= form_label('Actualizado: ', 'updated', array('class'=>'col-sm-2 control-label')); ?>
		<input type="text" name="updated" value="<?= date("d/m/Y - H:i",strtotime($registro->updated)); ?>" disabled/>
		<?= form_hidden('updated', $registro->updated); ?>
	</div>

	<hr>

	<div class="form-group">
		<div class="col-sm-offset-2">
			<?= form_button(array('type'=>'submit', 'content'=>'Aceptar', 'class'=>'btn btn-success')); ?>
			<?= anchor('menu/index', 'Cancelar',array('class'=>'btn btn-warning')); ?>
			<?= anchor('menu/delete/'.$registro->id, 'Eliminar',array('class'=>'btn btn-danger', 'onClick'=>"return confirm('¿Estas Seguro?');")); ?>
		</div>
	</div>
<?= form_close(); ?>