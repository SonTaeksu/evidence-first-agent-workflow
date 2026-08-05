namespace MinimalApp
{
    partial class MainForm
    {
        private System.ComponentModel.IContainer components = null;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }

            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        private void InitializeComponent()
        {
            this.panelInput = new System.Windows.Forms.Panel();
            this.lblName = new System.Windows.Forms.Label();
            this.txtName = new System.Windows.Forms.TextBox();
            this.btnGreet = new System.Windows.Forms.Button();
            this.lblStatus = new System.Windows.Forms.Label();
            this.panelInput.SuspendLayout();
            this.SuspendLayout();
            //
            // panelInput
            //
            this.panelInput.Location = new System.Drawing.Point(12, 12);
            this.panelInput.Name = "panelInput";
            this.panelInput.Size = new System.Drawing.Size(360, 40);
            this.panelInput.TabIndex = 0;
            this.panelInput.Controls.Add(this.lblName);
            this.panelInput.Controls.Add(this.txtName);
            //
            // lblName
            //
            this.lblName.AutoSize = true;
            this.lblName.Location = new System.Drawing.Point(3, 10);
            this.lblName.Name = "lblName";
            this.lblName.Size = new System.Drawing.Size(41, 13);
            this.lblName.TabIndex = 0;
            this.lblName.Text = "Name";
            //
            // txtName
            //
            this.txtName.Location = new System.Drawing.Point(56, 7);
            this.txtName.Name = "txtName";
            this.txtName.Size = new System.Drawing.Size(280, 20);
            this.txtName.TabIndex = 1;
            //
            // btnGreet
            //
            this.btnGreet.Location = new System.Drawing.Point(12, 62);
            this.btnGreet.Name = "btnGreet";
            this.btnGreet.Size = new System.Drawing.Size(96, 27);
            this.btnGreet.TabIndex = 1;
            this.btnGreet.Text = "Greet";
            this.btnGreet.UseVisualStyleBackColor = true;
            this.btnGreet.Click += new System.EventHandler(this.OnGreetClick);
            //
            // lblStatus
            //
            this.lblStatus.AutoSize = true;
            this.lblStatus.Location = new System.Drawing.Point(124, 69);
            this.lblStatus.Name = "lblStatus";
            this.lblStatus.Size = new System.Drawing.Size(0, 13);
            this.lblStatus.TabIndex = 2;
            //
            // MainForm
            //
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(384, 111);
            this.Controls.Add(this.panelInput);
            this.Controls.Add(this.btnGreet);
            this.Controls.Add(this.lblStatus);
            this.Name = "MainForm";
            this.Text = "Minimal App";
            this.panelInput.ResumeLayout(false);
            this.panelInput.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        #endregion

        private System.Windows.Forms.Panel panelInput;
        private System.Windows.Forms.Label lblName;
        private System.Windows.Forms.TextBox txtName;
        private System.Windows.Forms.Button btnGreet;
        private System.Windows.Forms.Label lblStatus;
    }
}
