package com.nju.net.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.Async;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RequestMapping(value = "/api")
@RestController
public class DemoApplication {

	public static String setSwitchScriptFullPath = "demo\\demo\\src\\main\\resources\\Telnet\\SwitchDemo.py";//设置交换机脚本目录
	public static String setRouterScriptFullPath = "demo\\demo\\src\\main\\resources\\Telnet\\RouterDemo.py";//设置路由器脚本目录

	public static void main(String[] args) {
		SpringApplication.run(DemoApplication.class, args);
	}

	@RequestMapping(value = "setSwitch", method = RequestMethod.POST)
	public String setSwitch(@RequestParam("host_ip") String hostIp,
							  @RequestParam("password_login") String passwordLogin,
							  @RequestParam("password_enable") String passwordEnable,
							  @RequestParam("vlan1") String vlan1,
							  @RequestParam("interface1") String interface1,
							  @RequestParam("vlan2") String vlan2,
							  @RequestParam("interface2") String interface2,
							  @RequestParam("interface_router") String interfaceRouter){
		doSetSwitch(hostIp, passwordLogin, passwordEnable, vlan1, interface1, vlan2, interface2, interfaceRouter);
		return "设置交换机成功！";
	}

	@RequestMapping(value = "setRouter", method = RequestMethod.POST)
	public String setRouter(@RequestParam("host_ip") String hostIp,
							@RequestParam("password_login") String passwordLogin,
							@RequestParam("password_enable") String passwordEnable,
							@RequestParam("gateway1") String gateway1,
							@RequestParam("mask1") String mask1,
							@RequestParam("vlan1") String vlan1,
							@RequestParam("gateway2") String gateway2,
							@RequestParam("mask2") String mask2,
							@RequestParam("vlan2") String vlan2){
		doSetRouter(hostIp, passwordLogin, passwordEnable, gateway1, mask1, vlan1, gateway2, mask2, vlan2);
		return "设置路由器成功！";
	}

	@Async("doSetSwitch")
	public void doSetSwitch(String hostIp,
							String passwordLogin,
							String passwordEnable,
							String vlan1,
							String interface1,
							String vlan2,
							String interface2,
							String interfaceRouter){
		try{
			String commands[] = {"python", setSwitchScriptFullPath, hostIp, passwordLogin, passwordEnable,
					vlan1, interface1, vlan2, interface2, interfaceRouter};
			Runtime.getRuntime().exec(commands);
		}catch (Exception e){
			e.printStackTrace();
		}
	}

	@Async("doSetRouter")
	public void doSetRouter(String hostIp,
							String passwordLogin,
							String passwordEnable,
							String gateway1,
							String mask1,
							String vlan1,
							String gateway2,
							String mask2,
							String vlan2){
		try{
			String commands[] = {"python", setRouterScriptFullPath, hostIp, passwordLogin, passwordEnable,
					gateway1, mask1, vlan1, gateway2, mask2, vlan2};
			Runtime.getRuntime().exec(commands);
		}catch (Exception e){
			e.printStackTrace();
		}
	}

	@RequestMapping(value = "/index")
	public String getHtml(){
		return "index";
	}
}
