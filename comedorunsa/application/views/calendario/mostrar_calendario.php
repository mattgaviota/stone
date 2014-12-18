<div class="jumbotron">
	<div class="row">
		<div class="col-md-8">
			<h2>Calendario académico</h2>
		</div>
	</div>
	<div class="row">
		<div class="col-md-7">
			<?= $calendario; ?>
			<script type="text/javascript">
				base_url = '<?=base_url(); ?>';
			</script>
			<script src="<?= base_url('js/calendario-ajax.js'); ?>"></script>
		</div>
		<div class="col-md-5">
			<div class="panel panel-info">
				<div class="panel-heading">
					<h3 class="panel-title">Panel info</h3>
				</div>
				<div class="panel-body">
					<?= form_open('index.php/calendario/actualizar', array('id'=>'resultadoCalendario')); ?>
					<?= form_close(); ?>
					<br>
					<span id="mensaje"></span>
				</div>
			</div>
		</div>
	</div>
</div>





