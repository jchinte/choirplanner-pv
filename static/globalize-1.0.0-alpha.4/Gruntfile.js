module.exports = function( grunt ) {

	"use strict";

	var isConnectTestRunning,
		rdefineEnd = /\}\);[^}\w]*$/,
		pkg = grunt.file.readJSON( "package.json" );

	function camelCase( input ) {
		return input.toLowerCase().replace( /[-/](.)/g, function( match, group1 ) {
			return group1.toUpperCase();
		});
	}

	function mountFolder( connect, path ) {
		return connect.static( require( "path" ).resolve( path ) );
	}

	function replaceConsts( content ) {
		return content

			// Replace Version
			.replace( /@VERSION/g, pkg.version )

			// Replace Date yyyy-mm-ddThh:mmZ
			.replace( /@DATE/g, ( new Date() ).toISOString().replace( /:\d+\.\d+Z$/, "Z" ) );
	}

	grunt.initConfig({
		pkg: pkg,
		connect: {
			options: {
				port: 9001,
				hostname: "localhost"
			},
			test: {
				options: {
					middleware: function ( connect ) {
						return [
							mountFolder( connect, "." ),
							mountFolder( connect, "test" )
						];
					}
				}
			}
		},
		jshint: {
			source: {
				src: [ "src/**/*.js", "!src/build/**" ],
				options: {
					jshintrc: "src/.jshintrc"
				}
			},
			grunt: {
				src: [ "Gruntfile.js" ],
				options: {
					jshintrc: ".jshintrc"
				}
			},
			test: {
				src: [ "test/*.js", "test/functional/**/*.js", "test/unit/**/*.js" ],
				options: {
					jshintrc: "test/.jshintrc"
				}
			},
			dist: {
				src: [ "dist/globalize*.js", "dist/globalize/*.js", "!dist/**/*.min.*js" ],
				options: {
					jshintrc: "src/.dist-jshintrc"
				}
			}
		},
		qunit: {
			functional: {
				options: {
					urls: [ "http://localhost:<%= connect.options.port %>/functional.html" ]
				}
			},
			unit: {
				options: {
					urls: [ "http://localhost:<%= connect.options.port %>/unit.html" ]
				}
			}
		},
		requirejs: {
			options: {
				dir: "dist/.build",
				appDir: "src",
				baseUrl: ".",
				optimize: "none",
				paths: {
					cldr: "../external/cldrjs/dist/cldr"
				},
				skipSemiColonInsertion: true,
				skipModuleInsertion: true,

				// Strip all definitions generated by requirejs.
				// Convert content as follows:
				// a) "Single return" means the module only contains a return statement that is converted to a var declaration.
				// b) "Not as simple as a single return" means the define wrappers are replaced by a function wrapper call and the returned value is assigned to a var.
				// c) "Module" means the define wrappers are removed, but content is untouched. Only for root id's (the ones in src, not in src's subpaths).
				onBuildWrite: function ( id, path, contents ) {
					var name = camelCase( id.replace( /util\/|common\//, "" ) );

					// 1, and 2: Remove define() wrap.
					// 3: Remove empty define()'s.
					contents = contents
						.replace( /define\([^{]*?{/, "" ) /* 1 */
						.replace( rdefineEnd, "" ) /* 2 */
						.replace( /define\(\[[^\]]+\]\)[\W\n]+$/, "" ); /* 3 */

					// Type b (not as simple as a single return)
					if ( [ "date/parse" ].indexOf( id ) !== -1 ) {
						contents = "var " + name + " = (function() {" +
							contents + "}());";
					}
					// Type a (single return)
					else if ( (/\//).test( id ) ) {
						contents = contents
							.replace( /\nreturn/, "\nvar " + name + " =" );
					}

					return contents;
				}
			},
			bundle: {
				options: {
					modules: [
						{
							name: "globalize",
							include: [ "core" ],
							exclude: [ "cldr", "cldr/event" ],
							create: true,
							override: {
								wrap: {
									startFile: "src/build/intro-core.js",
									endFile: "src/build/outro.js"
								}
							}
						},
						{
							name: "globalize.date",
							include: [ "date" ],
							exclude: [ "cldr", "cldr/supplemental", "./core" ],
							create: true,
							override: {
								wrap: {
									startFile: "src/build/intro-date.js",
									endFile: "src/build/outro.js"
								}
							}
						},
						{
							name: "globalize.number",
							include: [ "number" ],
							exclude: [ "cldr", "cldr/event", "./core" ],
							create: true,
							override: {
								wrap: {
									startFile: "src/build/intro-number.js",
									endFile: "src/build/outro.js"
								}
							}
						},
						{
							name: "globalize.message",
							include: [ "message" ],
							exclude: [ "cldr", "cldr/event", "./core" ],
							create: true,
							override: {
								wrap: {
									startFile: "src/build/intro-message.js",
									endFile: "src/build/outro.js"
								}
							}
						}
					]
				}
			}
		},
		watch: {
			files: [ "src/*.js", "test/functional/**/*.js", "test/unit/**/*.js", "test/*.html" ],
			tasks: [ "default" ]
		},
		copy: {
			options: {
				processContent: function( content ) {

					// Remove leftover define created during rjs build
					content = content.replace( /define\(".*/, "" );

					// Embed VERSION and DATE
					return replaceConsts( content );
				}
			},
			dist_core: {
				expand: true,
				cwd: "dist/.build/",
				src: [ "globalize.js" ],
				dest: "dist/"
			},
			dist_modules: {
				expand: true,
				cwd: "dist/.build/",
				src: [ "globalize*.js", "!globalize.js" ],
				dest: "dist/globalize",
				rename: function( dest, src ) {
					return require( "path" ).join( dest, src.replace( /globalize\./, "" ) );
				}
			},
			dist_allinone_node: {
				src: "src/build/allinone-node.js",
				dest: "dist/globalize-allinone-node.js"
			}
		},
		uglify: {
			options: {
				banner: replaceConsts( grunt.file.read( "src/build/intro.min.js" ) )
			},
			dist: {
				files: {
						"dist/globalize.min.js": [ "dist/globalize.js" ],
						"dist/globalize/date.min.js": [ "dist/globalize/date.js" ],
						"dist/globalize/number.min.js": [ "dist/globalize/number.js" ],
						"dist/globalize/message.min.js": [ "dist/globalize/message.js" ]
				}
			}
		},
		compare_size: {
			files: [
				"dist/globalize.min.js",
				"dist/globalize/*min.js"
			],
			options: {
				compress: {
					gz: function( fileContents ) {
						return require( "gzip-js" ).zip( fileContents, {} ).length;
					}
				}
			}
		},
		clean: {
			dist: [
				"dist"
			]
		},
		checkDependencies: {
			bower: {
				options: {
					packageManager: "bower"
				}
			},
			npm: {
				options: {
					packageManager: "npm"
				}
			}
		}
	});

	require( "matchdep" ).filterDev( "grunt-*" ).forEach( grunt.loadNpmTasks );

	grunt.registerTask( "test", function() {
		var args = [].slice.call( arguments );
		if ( !isConnectTestRunning ) {
			grunt.task.run( "checkDependencies" );
			grunt.task.run( "connect:test" );
			isConnectTestRunning = true;
		}
		grunt.task.run( [ "qunit" ].concat( args ).join( ":" ) );
	});

	// Default task.
	grunt.registerTask( "default", [
		"jshint:grunt",
		"jshint:source",
		"jshint:test",
		"test:unit",
		"clean",
		"requirejs",
		"copy",
		"jshint:dist",
		"test:functional",
		"uglify",
		"compare_size"
	] );

};
