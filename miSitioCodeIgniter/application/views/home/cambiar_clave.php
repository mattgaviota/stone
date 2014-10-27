<?= form_open('index.php/home/cambiando_clave', array('class'=>'form-horizontal')); ?>
	<legend>Cambiar Clave de acceso</legend>

	<?= my_validation_errors(validation_errors()); ?>

	<div class="row">
		<div class="form-group">
			<?= form_label('Clave Actual: ', 'clave_actual', array('class'=>'col-md-3 control-label')); ?>
			<div class="col-md-3">
				<?= form_input(array('class'=>'form-control','type'=>'password', 'name'=>'clave_actual', 'id'=>'clave_actual', 'value'=>set_value('clave_actual'))); ?>
			</div>		
		</div>
	</div>

	<div class="row">
		<div class="form-group">
			<?= form_label('Clave Nueva: ', 'clave_nueva', array('class'=>'col-md-3 control-label')); ?>
			<div class="col-md-3">
				<?= form_input(array('class'=>'form-control','type'=>'password', 'name'=>'clave_nueva', 'id'=>'clave_nueva', 'value'=>set_value('clave_nueva'))); ?>
			</div>		
		</div>
	</div>

	<div class="row">
		<div class="form-group">
			<?= form_label('Repetir Clave Nueva: ', 'clave_repetida', array('class'=>'col-md-3 control-label')); ?>
			<div class="col-md-3">
				<?= form_input(array('class'=>'form-control','type'=>'password', 'name'=>'clave_repetida', 'id'=>'clave_repetida', 'value'=>set_value('clave_repetida'))); ?>
			</div>		
		</div>
	</div>

	<hr>

	<div class="row">
		<div class="form-group">
			<div class="col-md-offset-2">
				<div class="col-md-6">
					<?= form_button(array('type'=>'submit', 'content'=>' Aceptar', 'class'=>'btn btn-success glyphicon glyphicon-ok')); ?>
	
					<?= anchor('home/index', ' Cancelar',array('class'=>'btn btn-default glyphicon glyphicon-remove')); ?>
				</div>
			</div>
		</div>
	</div>


<?= form_close(); ?>