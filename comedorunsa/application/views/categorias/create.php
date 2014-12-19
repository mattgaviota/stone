<?= form_open('index.php/categorias/insert', array('class'=>'form-horizontal jumbotron')); ?>
	<legend>Agregando un Registro</legend>

	<?= my_validation_errors(validation_errors()); ?>

	<div class="row">
		<div class="form-group">
			<?= form_label('Nombre: ', 'nombre', array('class'=>'col-md-2 control-label')); ?>
			<div class="col-md-3">
				<?= form_input(array('class'=>'form-control','type'=>'text', 'name'=>'nombre', 'id'=>'nombre','value'=>set_value('nombre'))); ?>
			</div>
		</div>
	</div>

	<hr>

	<div class="row">
		<div class="form-group">
			<div class="col-md-offset-1">
				<div class="col-md-6">
					<?= form_button(array('type'=>'submit', 'content'=>' Aceptar', 'class'=>'btn btn-success glyphicon glyphicon-ok')); ?>

					<?= anchor('categorias/index', ' Cancelar',array('class'=>'btn btn-default glyphicon glyphicon-remove')); ?>
				</div>
			</div>
		</div>	
	</div>

<?= form_close(); ?>