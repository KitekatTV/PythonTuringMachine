use pyo3::prelude::*;
use gtk::prelude::*;
use gtk::{Application, ApplicationWindow, Button, Label, Box, Orientation, gio::ApplicationFlags};
use lazy_static::lazy_static;
use std::sync::Mutex;
use regex::Regex;

const APP_ID: &str = "org.gtk_rs.Visualizer";

lazy_static! {
    static ref NAME: Mutex<String> = Mutex::new("Visualizer".to_string());
    static ref INPUT: Mutex<String> = Mutex::new("0".to_string());
    static ref OUTPUT: Mutex<String> = Mutex::new("0".to_string());
}

#[pyfunction]
fn display(name:String, input: String, output: String) {
    let mut parsed_input = "".to_string();
    let mut parsed_output = "".to_string();
    let re = Regex::new(r"[01]+").unwrap();
    for capture in re.captures_iter(&input) { parsed_input = parsed_input + &capture[0] + "|"; }
    for capture in re.captures_iter(&output) { parsed_output = parsed_output + &capture[0] + "|"; }

    *NAME.lock().unwrap() = name;
    *INPUT.lock().unwrap() = parsed_input;
    *OUTPUT.lock().unwrap() = parsed_output;

    let app = Application::builder()
        .application_id(APP_ID)
        .flags(ApplicationFlags::HANDLES_OPEN)
        .build();
    app.connect_open(build_ui);
    app.run();
}

fn build_ui(app: &Application, _files: &[gtk::gio::File], _arguments: &str) {
    let raw_input = INPUT.lock().unwrap();
    let input = str::replace(&raw_input, "|", " ");
    let input_value_label = Label::builder()
        .label(&input)
        .margin_top(12)
        .margin_bottom(12)
        .margin_start(12)
        .margin_end(12)
        .build();

    let raw_output = OUTPUT.lock().unwrap();
    let output = str::replace(&raw_output, "|", " ");
    let output_value_label = Label::builder()
        .label(&output)
        .margin_top(12)
        .margin_bottom(12)
        .margin_start(12)
        .margin_end(12)
        .build();
    
    let button = Button::builder()
        .label("To decimal")
        .margin_top(12)
        .margin_bottom(12)
        .margin_start(12)
        .margin_end(12)
        .build();

    let content = Box::new(Orientation::Vertical,0);
    content.append(&input_value_label);
    content.append(&output_value_label);
    content.append(&button);

    button.connect_clicked(move |button| {
        if button.label().as_deref().unwrap_or("default string") == "To decimal" {
            button.set_label("To binary");

            let mut input_text = "".to_string();
            let cur = input_value_label.label();
            let mut nums: Vec<&str> = cur.split(" ").collect();
            nums.pop();
            for num in nums {
                input_text = input_text + (i32::from_str_radix(&num, 2).unwrap()).to_string().as_str();
                input_text = input_text + " ";
            }
            input_value_label.set_label(&input_text);
            
            let mut output_text = "".to_string();
            let cur = output_value_label.label();
            let mut nums: Vec<&str> = cur.split(" ").collect();
            nums.pop();
            for num in nums {
                output_text = output_text + (i32::from_str_radix(&num, 2).unwrap()).to_string().as_str();
                output_text = output_text + " ";
            }
            output_value_label.set_label(&output_text);
        }
        else {
            button.set_label("To decimal");

            let mut text = "".to_string();
            let cur = input_value_label.label();
            let mut nums: Vec<&str> = cur.split(" ").collect();
            nums.pop();
            for num in nums {
                text = text + &format!("{:b}", &num.parse::<i32>().unwrap()).to_string();
                text = text + " ";
            }
            input_value_label.set_label(&text);

            let mut output_text = "".to_string();
            let cur = output_value_label.label();
            let mut nums: Vec<&str> = cur.split(" ").collect();
            nums.pop();
            for num in nums {
                output_text = output_text + &format!("{:b}", &num.parse::<i32>().unwrap()).to_string();
                output_text = output_text + " ";
            }
            output_value_label.set_label(&output_text);
        }
    });

    let name = NAME.lock().unwrap();
    let window = ApplicationWindow::builder()
        .application(app)
        .title(&name)
        .child(&content)
        .build();

    window.present();
}

#[pymodule]
fn numbers_gui(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(display, m)?)?;
    Ok(())
}
